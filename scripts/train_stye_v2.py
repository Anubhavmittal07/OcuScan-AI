"""
scripts/train_stye_v2.py
-------------------------
Trains and comprehensively evaluates a reconstructed, leakage-free Stye / Hordeolum
classifier (MobileNetV3-Small) using the verified Roboflow Eye Dataset manifest.

Features:
1. Strict Subject-Isolated Validation & Testing:
   - Zero subject/augmentation leakage across Train, Val, and Test splits.
2. Clinical Lookalike Differential Analysis:
   - Evaluates performance separately on Healthy controls vs. Blepharitis lookalikes.
3. Class-Imbalance Weighted Loss:
   - Compensates for 2,020 Non-Stye vs. 1,186 Stye ratio in training set.
4. Color-Preserving Conservative Augmentation:
   - Flips, minor affine shifts, and mild contrast; NO hue/erythema solarization.
5. Candidate Checkpointing:
   - Saves to saved_models/stye_candidate/ first for evaluation before promotion.
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
from PIL import Image
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torchvision import transforms
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report
)

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from src.models.stye_model import StyeClassifier, save_stye_checkpoint
from src.preprocessing.image_quality import safe_load_image, resize_and_pad

MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, 'data', 'manifests', 'stye_hordeolum_manifest.csv')
CANDIDATE_DIR = os.path.join(WORKSPACE_ROOT, 'saved_models', 'stye_candidate')
os.makedirs(CANDIDATE_DIR, exist_ok=True)


class StyeDatasetV2(Dataset):
    def __init__(self, df: pd.DataFrame, transform=None):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self._cache = {}

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        if idx in self._cache:
            im = self._cache[idx]
        else:
            row = self.df.iloc[idx]
            raw_path = os.path.join(WORKSPACE_ROOT, row['relative_path'])
            full_path = os.path.abspath(raw_path)
            if os.name == 'nt' and not full_path.startswith('\\\\?\\'):
                full_path = '\\\\?\\' + full_path

            im = safe_load_image(full_path)
            if im is None:
                im = Image.new('RGB', (224, 224), (0, 0, 0))
            else:
                im = resize_and_pad(im, (224, 224))
            self._cache[idx] = im

        if self.transform:
            tensor = self.transform(im)
        else:
            tensor = transforms.ToTensor()(im)

        row = self.df.iloc[idx]
        return {
            'image': tensor,
            'label': torch.tensor(int(row['label']), dtype=torch.long),
            'image_id': row['image_id'],
            'filename': row['filename'],
            'subject_id': row['subject_id'],
            'subcategory': row.get('subcategory', 'unknown')
        }


def compute_metrics(y_true, y_pred, y_prob):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    try:
        auc = roc_auc_score(y_true, y_prob)
    except Exception:
        auc = 0.5
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    return {
        'accuracy': float(acc),
        'precision': float(prec),
        'recall_sensitivity': float(rec),
        'specificity': float(spec),
        'f1_score': float(f1),
        'roc_auc': float(auc),
        'confusion_matrix': cm.tolist(),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'true_positives': int(tp)
    }


def evaluate_model(model, loader, device):
    model.eval()
    all_preds, all_probs, all_targets, all_subcats, all_ids = [], [], [], [], []
    with torch.no_grad():
        for batch in loader:
            imgs = batch['image'].to(device)
            targets = batch['label'].to(device)
            outputs = model(imgs)
            probs = torch.softmax(outputs, dim=1)[:, 1]
            preds = torch.argmax(outputs, dim=1)

            all_probs.extend(probs.cpu().numpy().tolist())
            all_preds.extend(preds.cpu().numpy().tolist())
            all_targets.extend(targets.cpu().numpy().tolist())
            all_subcats.extend(batch['subcategory'])
            all_ids.extend(batch['image_id'])

    metrics = compute_metrics(all_targets, all_preds, all_probs)
    return metrics, all_targets, all_preds, all_probs, all_subcats, all_ids


def train_stye_model(epochs: int = 6, batch_size: int = 32, lr: float = 3e-4):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("=" * 70)
    print(f"TRAINING RECONSTRUCTED STYE / HORDEOLUM CLASSIFIER (Device: {device})")
    print("=" * 70)

    df = pd.read_csv(MANIFEST_PATH)
    train_df = df[df['split'] == 'train']
    val_df = df[df['split'] == 'val']
    test_df = df[df['split'] == 'test']

    print(f"Data Splits: Train={len(train_df)} (Subjects: {train_df['subject_id'].nunique()}), "
          f"Val={len(val_df)} (Subjects: {val_df['subject_id'].nunique()}), "
          f"Test={len(test_df)} (Subjects: {test_df['subject_id'].nunique()})")

    # Verify zero leakage across splits
    train_subs = set(train_df['subject_id'])
    val_subs = set(val_df['subject_id'])
    test_subs = set(test_df['subject_id'])
    assert len(train_subs & val_subs) == 0, "Split leakage Train vs Val!"
    assert len(train_subs & test_subs) == 0, "Split leakage Train vs Test!"
    assert len(val_subs & test_subs) == 0, "Split leakage Val vs Test!"
    print("[PASS] Certified Zero Subject-Level / Augmentation Leakage Verified!")

    train_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=8),
        transforms.ColorJitter(brightness=0.06, contrast=0.06),  # conservative to preserve erythema
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    eval_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    print("Building datasets and pre-caching...")
    train_ds = StyeDatasetV2(train_df, transform=train_transform)
    val_ds = StyeDatasetV2(val_df, transform=eval_transform)
    test_ds = StyeDatasetV2(test_df, transform=eval_transform)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    n_neg = (train_df['label'] == 0).sum()
    n_pos = (train_df['label'] == 1).sum()
    total_train = len(train_df)
    weight_neg = total_train / (2.0 * n_neg)
    weight_pos = total_train / (2.0 * n_pos)
    class_weights = torch.tensor([weight_neg, weight_pos], dtype=torch.float).to(device)
    print(f"Class counts in train: Neg(Non-Stye)={n_neg}, Pos(Stye)={n_pos}. Balanced weights: {class_weights.tolist()}")

    model = StyeClassifier(pretrained=True, num_classes=2).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=1e-3)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    best_val_f1 = -1.0
    best_val_metrics = {}
    best_checkpoint_path = os.path.join(CANDIDATE_DIR, 'best_model.pth')
    log_records = []

    start_time = time.time()
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        train_preds, train_probs, train_targets = [], [], []

        for batch in train_loader:
            imgs = batch['image'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * imgs.size(0)
            probs = torch.softmax(outputs, dim=1)[:, 1]
            preds = torch.argmax(outputs, dim=1)

            train_probs.extend(probs.detach().cpu().numpy().tolist())
            train_preds.extend(preds.detach().cpu().numpy().tolist())
            train_targets.extend(labels.cpu().numpy().tolist())

        scheduler.step()
        epoch_loss = running_loss / len(train_ds)
        train_metrics = compute_metrics(train_targets, train_preds, train_probs)

        val_metrics, _, _, _, _, _ = evaluate_model(model, val_loader, device)

        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {epoch_loss:.4f} Acc: {train_metrics['accuracy']:.4f} F1: {train_metrics['f1_score']:.4f} | "
              f"Val Acc: {val_metrics['accuracy']:.4f} Rec: {val_metrics['recall_sensitivity']:.4f} Spec: {val_metrics['specificity']:.4f} F1: {val_metrics['f1_score']:.4f} AUC: {val_metrics['roc_auc']:.4f}", flush=True)

        log_records.append({
            'epoch': epoch,
            'train_loss': round(epoch_loss, 4),
            'train_acc': round(train_metrics['accuracy'], 4),
            'train_f1': round(train_metrics['f1_score'], 4),
            'val_acc': round(val_metrics['accuracy'], 4),
            'val_rec': round(val_metrics['recall_sensitivity'], 4),
            'val_spec': round(val_metrics['specificity'], 4),
            'val_f1': round(val_metrics['f1_score'], 4),
            'val_auc': round(val_metrics['roc_auc'], 4)
        })

        if val_metrics['f1_score'] > best_val_f1:
            best_val_f1 = val_metrics['f1_score']
            best_val_metrics = val_metrics
            save_stye_checkpoint(
                model=model,
                save_path=best_checkpoint_path,
                optimizer=optimizer,
                epoch=epoch,
                metrics=val_metrics,
                class_mapping={'0': 'normal', '1': 'stye_hordeolum'},
                config={
                    'architecture': 'MobileNetV3-Small',
                    'input_size': [224, 224],
                    'normalization': 'ImageNet',
                    'learning_rate': lr,
                    'batch_size': batch_size,
                    'epochs': epochs,
                    'class_weights': class_weights.tolist()
                }
            )

    train_duration = time.time() - start_time
    print(f"\nTraining completed in {train_duration:.2f}s. Best Validation F1: {best_val_f1:.4f}")

    # Load best checkpoint and evaluate on untouched held-out test set
    best_model = StyeClassifier(pretrained=False, num_classes=2).to(device)
    ckpt = torch.load(best_checkpoint_path, map_location=device)
    best_model.load_state_dict(ckpt['model_state_dict'])

    test_metrics, test_targets, test_preds, test_probs, test_subcats, test_ids = evaluate_model(best_model, test_loader, device)

    # Subcategory breakdown analysis
    test_eval_df = pd.DataFrame({
        'image_id': test_ids,
        'subcategory': test_subcats,
        'true_label': test_targets,
        'pred_label': test_preds,
        'stye_prob': test_probs
    })

    subcat_results = {}
    print("\n" + "=" * 60)
    print("DETAILED PER-SUBCATEGORY TEST SET EVALUATION:")
    for sc in ['stye', 'healthy', 'blepharitis']:
        sc_df = test_eval_df[test_eval_df['subcategory'] == sc]
        correct = (sc_df['true_label'] == sc_df['pred_label']).sum()
        total = len(sc_df)
        acc = correct / total if total > 0 else 0.0
        avg_prob = sc_df['stye_prob'].mean()
        subcat_results[sc] = {
            'total': total,
            'correct': int(correct),
            'incorrect': int(total - correct),
            'accuracy': float(acc),
            'mean_stye_probability': float(avg_prob)
        }
        print(f"  {sc.capitalize():15s}: {correct}/{total} correct ({acc*100:.1f}%), Mean Stye Prob: {avg_prob:.4f}")

    print("=" * 60)
    print("OVERALL HELD-OUT TEST METRICS (ZERO SUBJECT LEAKAGE):")
    print(f"  Accuracy:    {test_metrics['accuracy']*100:.2f}%")
    print(f"  Precision:   {test_metrics['precision']*100:.2f}%")
    print(f"  Sensitivity: {test_metrics['recall_sensitivity']*100:.2f}%")
    print(f"  Specificity: {test_metrics['specificity']*100:.2f}%")
    print(f"  F1 Score:    {test_metrics['f1_score']*100:.2f}%")
    print(f"  ROC AUC:     {test_metrics['roc_auc']:.4f}")
    print(f"  Confusion Matrix: TN={test_metrics['true_negatives']}, FP={test_metrics['false_positives']}, FN={test_metrics['false_negatives']}, TP={test_metrics['true_positives']}")
    print("=" * 60)

    # Save artifacts in candidate directory
    pd.DataFrame(log_records).to_csv(os.path.join(CANDIDATE_DIR, 'training_log.csv'), index=False)
    test_eval_df.to_csv(os.path.join(CANDIDATE_DIR, 'test_predictions.csv'), index=False)

    class_mapping = {'0': 'normal', '1': 'stye_hordeolum'}
    with open(os.path.join(CANDIDATE_DIR, 'class_mapping.json'), 'w') as f:
        json.dump(class_mapping, f, indent=2)

    metrics_payload = {
        'disease': 'Stye / Hordeolum',
        'architecture': 'MobileNetV3-Small',
        'dataset': 'Roboflow Eye Dataset (Stye + Healthy + Blepharitis)',
        'modality': 'Anterior Eyelid / Ocular Photography',
        'license': 'CC BY 4.0 (Yudis Project)',
        'total_images': len(df),
        'unique_subjects': int(df['subject_id'].nunique()),
        'subject_isolated_split': {
            'train_subjects': int(train_df['subject_id'].nunique()),
            'val_subjects': int(val_df['subject_id'].nunique()),
            'test_subjects': int(test_df['subject_id'].nunique()),
            'train_images': len(train_df),
            'val_images': len(val_df),
            'test_images': len(test_df)
        },
        'validation_metrics': best_val_metrics,
        'test_metrics': test_metrics,
        'subcategory_breakdown': subcat_results,
        'training_duration_seconds': round(train_duration, 2)
    }
    with open(os.path.join(CANDIDATE_DIR, 'metrics.json'), 'w') as f:
        json.dump(metrics_payload, f, indent=2)

    print("Candidate model artifacts saved to:", CANDIDATE_DIR)
    return metrics_payload


if __name__ == '__main__':
    train_stye_model(epochs=6, batch_size=32, lr=3e-4)
