"""
scripts/prepare_stye_dataset_v2.py
-----------------------------------
Audits, cleans, and builds a strict, leakage-free manifest for the Stye / Hordeolum
classification model using the Roboflow Eye Dataset candidate.

Clinical Design:
1. Target: Binary classification of acute Stye / Hordeolum (label 1) vs. Non-Stye (label 0).
2. Positive Cohort: Eyelid lesions verified as focal hordeolum / stye.
3. Negative Cohort:
   - Healthy anterior ocular controls from the identical acquisition/camera distribution.
   - Blepharitis cases (essential clinical lookalike: diffuse eyelid margin erythema/crusting
     without focal nodular stye abscess) to prevent false-positive over-triggering.
4. Leakage-Free Splitting:
   - Partitioning is strictly performed at the subject / base-image level.
   - All augmented variations of any base image (.rf.xxxxx) reside exclusively in the same partition.
   - 70% Train, 15% Validation, 15% Test.
   - Zero overlap of subjects across train, val, and test.
"""

import os
import sys
import hashlib
from pathlib import Path
from collections import Counter
import numpy as np
import pandas as pd
from PIL import Image

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

RAW_DATASET_DIR = os.path.join(WORKSPACE_ROOT, 'data', 'raw', 'roboflow_eye_dataset')
MANIFEST_OUT = os.path.join(WORKSPACE_ROOT, 'data', 'manifests', 'stye_hordeolum_manifest.csv')


def compute_md5(file_path: str) -> str:
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_base_id(filename: str) -> str:
    if '.rf.' in filename:
        return filename.split('.rf.')[0]
    return os.path.splitext(filename)[0]


def collect_class_records(raw_folder_name: str, binary_label: int, binary_class_name: str, subcategory: str, id_prefix: str):
    records = []
    splits = ['train', 'valid', 'test']
    for s in splits:
        dir_path = os.path.join(RAW_DATASET_DIR, s, raw_folder_name)
        if not os.path.exists(dir_path):
            continue
        for fn in sorted(os.listdir(dir_path)):
            if not fn.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            abs_path = os.path.join(dir_path, fn)
            # Use extended path on Windows for long paths
            long_abs = '\\\\?\\' + os.path.abspath(abs_path)
            try:
                with open(long_abs, 'rb') as f:
                    md5_val = hashlib.md5(f.read()).hexdigest()
                with Image.open(long_abs) as im:
                    w, h = im.size
            except Exception as e:
                print(f"Skipping unreadable/corrupt image {abs_path}: {e}")
                continue

            rel_path = os.path.relpath(abs_path, WORKSPACE_ROOT).replace('\\', '/')
            base_id = get_base_id(fn)
            subject_id = f"{id_prefix}_{base_id}"

            records.append({
                'image_id': f"stye_v2_{Path(fn).stem}",
                'filename': fn,
                'relative_path': rel_path,
                'subject_id': subject_id,
                'label': binary_label,
                'class_name': binary_class_name,
                'subcategory': subcategory,
                'dataset_source': 'Roboflow_Eye_Dataset_v1',
                'modality': 'anterior_ocular_eyelid_photography',
                'md5': md5_val,
                'width': w,
                'height': h,
                'aspect_ratio': round(w / h, 4)
            })
    return records


def main():
    print("=" * 70)
    print("OcuScan AI - Stye / Hordeolum Dataset Preparation & Leakage Audit")
    print("=" * 70)

    if not os.path.exists(RAW_DATASET_DIR):
        raise FileNotFoundError(f"Roboflow dataset directory not found at: {RAW_DATASET_DIR}")

    print("Collecting and validating candidate classes from Roboflow Eye Dataset...")
    # 1. Stye (Positive)
    stye_records = collect_class_records('Stye', 1, 'stye_hordeolum', 'stye', 'stye_subj')
    print(f"Loaded {len(stye_records)} Stye images across {len(set(r['subject_id'] for r in stye_records))} unique subjects.")

    # 2. Healthy Controls (Negative)
    healthy_records = collect_class_records('Healthy', 0, 'non_stye', 'healthy', 'healthy_subj')
    print(f"Loaded {len(healthy_records)} Healthy control images across {len(set(r['subject_id'] for r in healthy_records))} unique subjects.")

    # 3. Blepharitis Lookalikes (Negative - Clinical Differential Diagnosis)
    bleph_records = collect_class_records('Blepharitis', 0, 'non_stye', 'blepharitis', 'bleph_subj')
    print(f"Loaded {len(bleph_records)} Blepharitis images across {len(set(r['subject_id'] for r in bleph_records))} unique subjects.")

    all_records = stye_records + healthy_records + bleph_records
    df = pd.DataFrame(all_records)

    print("\nTotal dataset volume:")
    print(f"  Total images: {len(df)}")
    print(f"  Unique subjects: {df['subject_id'].nunique()}")
    print("\nClass breakdown:")
    print(df['class_name'].value_counts())
    print("\nSubcategory breakdown:")
    print(df['subcategory'].value_counts())

    # Subject-Isolated Leakage-Free Splitting
    print("\n" + "-" * 50)
    print("Performing strict subject-isolated 70/15/15 split...")
    rng = np.random.RandomState(42)

    subject_split_map = {}
    for subcat in ['stye', 'healthy', 'blepharitis']:
        subcat_df = df[df['subcategory'] == subcat]
        unique_subjects = sorted(list(subcat_df['subject_id'].unique()))
        rng.shuffle(unique_subjects)

        n = len(unique_subjects)
        n_train = int(round(n * 0.70))
        n_val = int(round(n * 0.15))

        train_s = unique_subjects[:n_train]
        val_s = unique_subjects[n_train:n_train + n_val]
        test_s = unique_subjects[n_train + n_val:]

        for s in train_s:
            subject_split_map[s] = 'train'
        for s in val_s:
            subject_split_map[s] = 'val'
        for s in test_s:
            subject_split_map[s] = 'test'

    df['split'] = df['subject_id'].map(subject_split_map)

    # Verification of zero leakage
    train_subs = set(df[df['split'] == 'train']['subject_id'])
    val_subs = set(df[df['split'] == 'val']['subject_id'])
    test_subs = set(df[df['split'] == 'test']['subject_id'])

    assert len(train_subs & val_subs) == 0, f"LEAKAGE DETECTED between Train and Val: {len(train_subs & val_subs)}"
    assert len(train_subs & test_subs) == 0, f"LEAKAGE DETECTED between Train and Test: {len(train_subs & test_subs)}"
    assert len(val_subs & test_subs) == 0, f"LEAKAGE DETECTED between Val and Test: {len(val_subs & test_subs)}"
    print("[PASS] ZERO SUBJECT OR AUGMENTATION LEAKAGE VERIFIED!")

    print("\nSplit statistics (Images):")
    print(pd.crosstab(df['split'], df['class_name'], margins=True))

    print("\nSplit statistics by Subcategory:")
    print(pd.crosstab(df['split'], df['subcategory'], margins=True))

    # Save manifest
    os.makedirs(os.path.dirname(MANIFEST_OUT), exist_ok=True)
    df.to_csv(MANIFEST_OUT, index=False)
    print(f"\nManifest successfully written to: {MANIFEST_OUT}")


if __name__ == '__main__':
    main()
