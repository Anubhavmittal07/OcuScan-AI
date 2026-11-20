import os
import hashlib
import pandas as pd
from PIL import Image

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLEAN_DIR = os.path.join(WORKSPACE_ROOT, "data", "raw", "catscreen", "Data2025-main", "Clean")
IMG_DIR = os.path.join(CLEAN_DIR, "Clean images")
MANIFEST_OUT = os.path.join(WORKSPACE_ROOT, "data", "manifests", "catscreen_clean_manifest.csv")

records = []
for split_name, excel_file in [("train", "train.xlsx"), ("val", "val.xlsx"), ("test", "test.xlsx")]:
    excel_path = os.path.join(CLEAN_DIR, excel_file)
    df = pd.read_excel(excel_path)
    for idx, row in df.iterrows():
        fname = str(row["filename"]).strip()
        img_path = os.path.join(IMG_DIR, fname)
        if not os.path.exists(img_path):
            print(f"Warning: image {img_path} not found!")
            continue

        diag = str(row["diagnosis"]).strip()
        cat_type = str(row.get("catataract_type", "")).strip()
        illum = str(row.get("slit_lamp_illumination_type", "")).strip()
        quality = str(row.get("image_quality", "")).strip()
        cat_grade = str(row.get("cataract_grade", "")).strip()
        sub_id = str(row["id"]).strip()

        # Binary label: 1 = Cataract, 0 = Non-Cataract (Normal or Pseudophakic artificial lens)
        is_cataract = 1 if diag == "Cataract" else 0
        class_name = "nuclear_cataract" if is_cataract == 1 else "normal_clear_lens"

        # Compute SHA-256 and get dimensions
        with open(img_path, "rb") as f:
            data = f.read()
            sha256 = hashlib.sha256(data).hexdigest()

        with Image.open(img_path) as im:
            w, h = im.size

        rel_path = os.path.relpath(img_path, WORKSPACE_ROOT).replace("\\", "/")

        records.append({
            "image_id": f"catscreen_{sub_id}_{os.path.splitext(fname)[0]}",
            "filename": fname,
            "relative_path": rel_path,
            "patient_id": f"catscreen_{sub_id}",
            "raw_subject_id": sub_id,
            "eye_side": str(row.get("eye_side", "unspecified")),
            "diagnosis": diag,
            "cataract_type": cat_type,
            "cataract_grade": cat_grade,
            "slit_lamp_illumination": illum,
            "image_quality": quality,
            "label": is_cataract,
            "class_name": class_name,
            "dataset_source": "CatScreen (IAB Lab, IIT Jodhpur)",
            "modality": "Remidio Portable Slit Lamp PSL-D20",
            "width": w,
            "height": h,
            "aspect_ratio": round(w / h, 4),
            "sha256": sha256,
            "split": split_name
        })

out_df = pd.DataFrame(records)
os.makedirs(os.path.dirname(MANIFEST_OUT), exist_ok=True)
out_df.to_csv(MANIFEST_OUT, index=False)
print(f"Saved {len(out_df)} records to {MANIFEST_OUT}")
print("Split counts:\n", out_df["split"].value_counts())
print("Label counts:\n", out_df["label"].value_counts())
print("Class counts by split:\n", pd.crosstab(out_df["split"], out_df["class_name"]))
