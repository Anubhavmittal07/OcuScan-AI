import os
import pandas as pd

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CATSCREEN_CSV = os.path.join(WORKSPACE_ROOT, "data", "manifests", "catscreen_clean_manifest.csv")
NC_CSV = os.path.join(WORKSPACE_ROOT, "data", "manifests", "nuclear_cataract_manifest.csv")
OUT_CSV = os.path.join(WORKSPACE_ROOT, "data", "manifests", "cataract_multicenter_manifest.csv")

df_cat = pd.read_csv(CATSCREEN_CSV)
df_nc = pd.read_csv(NC_CSV)

# Harmonize columns
common_cols = [
    "image_id", "filename", "relative_path", "patient_id",
    "label", "class_name", "dataset_source", "modality", "width", "height", "aspect_ratio", "split"
]

sub_cat = df_cat[common_cols].copy()
sub_nc = df_nc[common_cols].copy()

# Combine
combined = pd.concat([sub_cat, sub_nc], ignore_index=True)

# Verify zero patient overlap across splits
train_pts = set(combined[combined['split'] == 'train']['patient_id'])
val_pts = set(combined[combined['split'] == 'val']['patient_id'])
test_pts = set(combined[combined['split'] == 'test']['patient_id'])

assert len(train_pts.intersection(val_pts)) == 0, "Patient leakage in train-val!"
assert len(train_pts.intersection(test_pts)) == 0, "Patient leakage in train-test!"
assert len(val_pts.intersection(test_pts)) == 0, "Patient leakage in val-test!"

combined.to_csv(OUT_CSV, index=False)
print(f"Combined multicenter manifest saved: {len(combined)} images across {combined['patient_id'].nunique()} unique patients.")
print("Class breakdown by split:\n", pd.crosstab(combined['split'], combined['class_name']))
print("Dataset sources:\n", combined['dataset_source'].value_counts())
