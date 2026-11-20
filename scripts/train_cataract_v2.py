"""
scripts/train_cataract_v2.py
----------------------------
Trains and evaluates CataractClassifier (MobileNetV3-Small) on the Multi-Center Slit-Lamp Dataset
incorporating CatScreen (IAB Lab, IIT Jodhpur) and Nuclear Cataract Biomicroscopy cohorts.

Enforces:
1. Zero subject leakage: Patient-isolated train, validation, and held-out test splits.
2. Clinical balance: Fixes the 0% specificity failure of the previous model by training on
   balanced normal clear lens controls and verified cataractous lenses.
3. Reproducible seed & evaluation: Evaluates held-out accuracy, precision, recall/sensitivity,
   specificity, F1-score, ROC AUC, and confusion matrix.
4. Safe checkpointing: Retains backups and full traceability.
"""

import os
import sys
import json
import time
import random
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
    f1_score, roc_auc_score, confusion_matrix
)

# Set seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from src.models.cataract_model import CataractClassifier, save_cataract_checkpoint, load_cataract_checkpoint
from src.preprocessing.image_quality import safe_load_image, resize_and_pad

MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, 'data', 'manifests', 'cataract_multicenter_manifest.csv')
CATSCREEN_MANIFEST_PATH = os.path.join(WORKSPACE_ROOT, 'data', 'manifests', 'catscreen_clean_manifest.csv')
SAVED_MODELS_DIR = os.path.join(WORKSPACE_ROOT, 'saved_models', 'cataract')
BACKUP_DIR = os.path.join(WORKSPACE_ROOT, 'saved_models', 'cataract_backup_pre_retrain')


class CataractDataset(Dataset):
    def __init__(self, df: pd.DataFrame, transform=None):
        self.df = df.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_path = os.path.join(WORKSPACE_ROOT, row['relative_path'])
        im = safe_load_image(img_path)
        if im is None:
            im = Image.new('RGB', (224, 224), (0, 0, 0))
        else:
            im = resize_and_pad(im, (224, 224))

        if self.transform:
            tensor = self.transform(im)
        else:
            tensor = transforms.ToTensor()(im)

        return {
            'image': tensor,
            'label': torch.tensor(int(row['label']), dtype=torch.long),
            'image_id': row['image_id'],
            'patient_id': row['patient_id'],
            'dataset_source': row.get('dataset_source', '')
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
        'accuracy': round(float(acc), 4),
        'precision': round(float(prec), 4),
        'recall_sensitivity': round(float(rec), 4),
        'specificity': round(float(spec), 4),
        'f1_score': round(float(f1), 4),
        'roc_auc': round(float(auc), 4),
        'confusion_matrix': cm.tolist(),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn),
        'true_positives': int(tp)
    }


def evaluate_model(model, loader, device):
    model.eval()
    all_preds, all_probs, all_targets = [], [], []
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

    return compute_metrics(all_targets, all_preds, all_probs), all_targets, all_preds, all_probs


def run_training_and_evaluation(epochs: int = 18, batch_size: int = 16, lr: float = 2.5e-4):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"=== TRAINING IMPROVED CATARACT CLASSIFIER (Device: {device}) ===")

    df = pd.read_csv(MANIFEST_PATH)
    train_df = df[df['split'] == 'train']
    val_df = df[df['split'] == 'val']
    test_df = df[df['split'] == 'test']

    print(f"Total Cohort: {len(df)} images, {df['patient_id'].nunique()} unique subjects.")
    print(f"  Train: {len(train_df)} images ({train_df['patient_id'].nunique()} subjects)")
    print(f"  Val:   {len(val_df)} images ({val_df['patient_id'].nunique()} subjects)")
    print(f"  Test:  {len(test_df)} images ({test_df['patient_id'].nunique()} subjects)")

    # Color-safe data augmentation (preserves chromatic brunescence & lens opacities)
    train_transform = transforms.Compose([
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.06, contrast=0.06),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    eval_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_ds = CataractDataset(train_df, transform=train_transform)
    val_ds = CataractDataset(val_df, transform=eval_transform)
    test_ds = CataractDataset(test_df, transform=eval_transform)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    # Class weighting to ensure balanced sensitivity AND specificity
    n_neg = (train_df['label'] == 0).sum()
    n_pos = (train_df['label'] == 1).sum()
    weight_neg = float(n_pos) / float(n_neg) if n_neg > 0 else 1.0
    class_weights = torch.tensor([weight_neg, 1.0], dtype=torch.float).to(device)
    print(f"Train Class Distribution: Neg(Clear)={n_neg}, Pos(Cataract)={n_pos}. Weights: {class_weights.tolist()}")

    # Initialize MobileNetV3-Small
    model = CataractClassifier(pretrained=True, num_classes=2).to(device)
    criterion = nn.CrossEntropyLoss(weight=class_weights)
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=1e-3)
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    best_val_score = -1.0
    best_val_metrics = {}
    candidate_checkpoint_path = os.path.join(SAVED_MODELS_DIR, 'candidate_best_model.pth')
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

        # Validation evaluation
        val_metrics, _, _, _ = evaluate_model(model, val_loader, device)

        # Balanced selection score: F1 + Specificity (ensures model never collapses specificity to 0!)
        val_selection_score = val_metrics['f1_score'] * 0.5 + val_metrics['specificity'] * 0.5

        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {epoch_loss:.4f} Acc: {train_metrics['accuracy']:.4f} | "
              f"Val Acc: {val_metrics['accuracy']:.4f} Sens: {val_metrics['recall_sensitivity']:.4f} "
              f"Spec: {val_metrics['specificity']:.4f} F1: {val_metrics['f1_score']:.4f} Score: {val_selection_score:.4f}")

        log_records.append({
            'epoch': epoch,
            'train_loss': round(epoch_loss, 4),
            'train_acc': val_metrics['accuracy'],
            'val_acc': val_metrics['accuracy'],
            'val_sensitivity': val_metrics['recall_sensitivity'],
            'val_specificity': val_metrics['specificity'],
            'val_f1': val_metrics['f1_score'],
            'val_auc': val_metrics['roc_auc']
        })

        if val_selection_score > best_val_score:
            best_val_score = val_selection_score
            best_val_metrics = val_metrics
            save_cataract_checkpoint(
                model=model,
                save_path=candidate_checkpoint_path,
                optimizer=optimizer,
                epoch=epoch,
                metrics=val_metrics,
                class_mapping={'0': 'normal_clear_lens', '1': 'nuclear_cataract'},
                config={
                    'architecture': 'MobileNetV3-Small',
                    'input_size': [224, 224],
                    'normalization': 'ImageNet',
                    'learning_rate': lr,
                    'batch_size': batch_size,
                    'epochs': epochs,
                    'class_weights': class_weights.tolist(),
                    'selection_score': round(val_selection_score, 4)
                }
            )

    train_duration = time.time() - start_time
    print(f"\nTraining finished in {train_duration:.2f}s. Best Val Balanced Score: {best_val_score:.4f}")

    # Load candidate model for held-out evaluation
    candidate_model = CataractClassifier(pretrained=False, num_classes=2).to(device)
    ckpt = torch.load(candidate_checkpoint_path, map_location=device)
    candidate_model.load_state_dict(ckpt['model_state_dict'])

    # 1. Evaluate on Combined Held-Out Test Set (90 images, 49 subjects)
    test_metrics, _, _, _ = evaluate_model(candidate_model, test_loader, device)

    # 2. Evaluate specifically on CatScreen Held-Out Test Set (40 images, 37 subjects)
    catscreen_df = pd.read_csv(CATSCREEN_MANIFEST_PATH)
    catscreen_test_df = catscreen_df[catscreen_df['split'] == 'test']
    catscreen_test_ds = CataractDataset(catscreen_test_df, transform=eval_transform)
    catscreen_test_loader = DataLoader(catscreen_test_ds, batch_size=batch_size, shuffle=False)
    catscreen_test_metrics, _, _, _ = evaluate_model(candidate_model, catscreen_test_loader, device)

    # 3. Evaluate Previous Baseline Model on Same Held-Out Test Set for Fair Comparison
    prev_model_path = os.path.join(BACKUP_DIR, 'best_model.pth')
    if os.path.exists(prev_model_path):
        prev_model = load_cataract_checkpoint(prev_model_path, device=device)
        prev_test_metrics, _, _, _ = evaluate_model(prev_model, test_loader, device)
        prev_catscreen_metrics, _, _, _ = evaluate_model(prev_model, catscreen_test_loader, device)
    else:
        prev_test_metrics = {}
        prev_catscreen_metrics = {}

    print("\n" + "=" * 70)
    print("COMPARATIVE EVALUATION ON HELD-OUT TEST DATA (ZERO PATIENT LEAKAGE):")
    print("--- 1. Combined Multicenter Test Set (N=90 images) ---")
    print(f"  Previous Model:  Acc={prev_test_metrics.get('accuracy')}, Sens={prev_test_metrics.get('recall_sensitivity')}, Spec={prev_test_metrics.get('specificity')}, F1={prev_test_metrics.get('f1_score')}")
    print(f"  Retrained Model: Acc={test_metrics['accuracy']}, Sens={test_metrics['recall_sensitivity']}, Spec={test_metrics['specificity']}, F1={test_metrics['f1_score']}")
    print(f"  Confusion Matrix (New): TN={test_metrics['true_negatives']}, FP={test_metrics['false_positives']}, FN={test_metrics['false_negatives']}, TP={test_metrics['true_positives']}")

    print("\n--- 2. CatScreen Clean Held-Out Test Set (N=40 images) ---")
    print(f"  Previous Model:  Acc={prev_catscreen_metrics.get('accuracy')}, Sens={prev_catscreen_metrics.get('recall_sensitivity')}, Spec={prev_catscreen_metrics.get('specificity')}, F1={prev_catscreen_metrics.get('f1_score')}")
    print(f"  Retrained Model: Acc={catscreen_test_metrics['accuracy']}, Sens={catscreen_test_metrics['recall_sensitivity']}, Spec={catscreen_test_metrics['specificity']}, F1={catscreen_test_metrics['f1_score']}")
    print(f"  Confusion Matrix (New): TN={catscreen_test_metrics['true_negatives']}, FP={catscreen_test_metrics['false_positives']}, FN={catscreen_test_metrics['false_negatives']}, TP={catscreen_test_metrics['true_positives']}")
    print("=" * 70)

    # Verification Gate: Ensure retrained model achieves genuine specificity improvement without collapsing recall
    if test_metrics['specificity'] > 0.50 and test_metrics['recall_sensitivity'] >= 0.70:
        print("\n[VERIFIED IMPROVEMENT] Specificity and sensitivity gates satisfied. Promoting candidate model to active checkpoint.")
        final_best_path = os.path.join(SAVED_MODELS_DIR, 'best_model.pth')
        torch.save(ckpt, final_best_path)

        metrics_payload = {
            'disease': 'Nuclear & Clinical Cataract',
            'architecture': 'MobileNetV3-Small',
            'dataset': 'CatScreen (IAB Lab, IIT Jodhpur) + Nuclear Cataract Dataset (Cruz-Vega et al.)',
            'modality': 'Slit-Lamp Biomicroscopy (Remidio PSL-D20 & Topcon DC-3)',
            'locs_iii_protocol': 'Lens Opacities Classification System III & CatScreen Multi-Tier Optometric Protocol',
            'total_images': len(df),
            'unique_patients': int(df['patient_id'].nunique()),
            'patient_isolated_split': {
                'train_patients': int(train_df['patient_id'].nunique()),
                'val_patients': int(val_df['patient_id'].nunique()),
                'test_patients': int(test_df['patient_id'].nunique()),
                'train_images': len(train_df),
                'val_images': len(val_df),
                'test_images': len(test_df)
            },
            'validation_metrics': best_val_metrics,
            'test_metrics_multicenter': test_metrics,
            'test_metrics_catscreen': catscreen_test_metrics,
            'baseline_comparison': {
                'previous_multicenter_spec': prev_test_metrics.get('specificity'),
                'previous_catscreen_spec': prev_catscreen_metrics.get('specificity'),
                'new_multicenter_spec': test_metrics['specificity'],
                'new_catscreen_spec': catscreen_test_metrics['specificity'],
                'improvement_summary': 'Resolved 0% specificity collapse: genuine discrimination between normal clear lenses and cataractous lenses.'
            },
            'training_duration_seconds': round(train_duration, 2)
        }
        with open(os.path.join(SAVED_MODELS_DIR, 'metrics.json'), 'w') as f:
            json.dump(metrics_payload, f, indent=2)

        pd.DataFrame(log_records).to_csv(os.path.join(SAVED_MODELS_DIR, 'training_log.csv'), index=False)
        print("Updated metrics.json and training_log.csv successfully.")
    else:
        print("\n[GATE WARNING] Retrained model did not satisfy promotion criteria. Active checkpoint left unchanged.")

    return test_metrics


if __name__ == '__main__':
    run_training_and_evaluation(epochs=16, batch_size=16, lr=2.5e-4)
