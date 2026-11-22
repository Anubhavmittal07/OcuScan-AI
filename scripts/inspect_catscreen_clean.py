import pandas as pd
import os

clean_dir = 'data/raw/catscreen/Data2025-main/Clean'
dfs = []
for split, fname in [('train', 'train.xlsx'), ('val', 'val.xlsx'), ('test', 'test.xlsx')]:
    df = pd.read_excel(os.path.join(clean_dir, fname))
    df['official_split'] = split
    dfs.append(df)

full_clean = pd.concat(dfs, ignore_index=True)
print(f"Total Clean Images: {len(full_clean)}")
print(f"Unique Subject IDs: {full_clean['id'].nunique()}")
print("\n--- Diagnosis distribution ---")
print(full_clean['diagnosis'].value_counts(dropna=False))
print("\n--- Cataract type distribution ---")
print(full_clean['catataract_type'].value_counts(dropna=False))
print("\n--- Slit-lamp illumination type distribution ---")
print(full_clean['slit_lamp_illumination_type'].value_counts(dropna=False))
print("\n--- Image quality distribution ---")
print(full_clean['image_quality'].value_counts(dropna=False))
print("\n--- Split distribution by Subject ID ---")
for sp in ['train', 'val', 'test']:
    sub_df = full_clean[full_clean['official_split'] == sp]
    print(f"{sp}: {len(sub_df)} images, {sub_df['id'].nunique()} unique subjects")

# Check subject overlap across splits
train_ids = set(full_clean[full_clean['official_split'] == 'train']['id'])
val_ids = set(full_clean[full_clean['official_split'] == 'val']['id'])
test_ids = set(full_clean[full_clean['official_split'] == 'test']['id'])

overlap_tr_val = train_ids.intersection(val_ids)
overlap_tr_te = train_ids.intersection(test_ids)
overlap_val_te = val_ids.intersection(test_ids)
print(f"\nSubject Overlap in Official Split: Train-Val={len(overlap_tr_val)}, Train-Test={len(overlap_tr_te)}, Val-Test={len(overlap_val_te)}")
