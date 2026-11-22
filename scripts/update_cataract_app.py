import os

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_cataract = """    # 4. Cataract (Nuclear Cataract Slit-Lamp) (MobileNetV3-Small)
    cataract_metrics = {
        "id": "model_d_cataract",
        "title": "Nuclear Cataract",
        "subtitle": "(Lens Opacity Classifier)",
        "architecture": "MobileNetV3-Small",
        "checkpoint_path": os.path.join(saved_dir, "cataract", "best_model.pth"),
        "dataset": "Nuclear Cataract Dataset (Cruz-Vega / Ignatowicz)",
        "lifecycle_status": "Available for Evaluation",
        "status_code": "available_for_evaluation",
        "status_label": "Available for Evaluation",
        "description": "Identifies lens opacification and nuclear cataract from anterior segment images.",
        "metrics_type": "classification",
        "accuracy": 0.727,
        "precision": 0.746,
        "recall_sensitivity": 0.697,
        "specificity": 0.757,
        "f1_score": 0.721,
        "roc_auc": 0.910,
        "test_samples": 750,
        "confusion_matrix": [[280, 90], [115, 265]],
        "labels": ["Normal", "Cataract"],
        "color_max": 300,
        "last_updated": "28 Oct 2026",
        "non_production_cause": "Held-out test accuracy is 72.7% and ROC-AUC is 0.910 on slit-lamp images. Slit-lamp optical requirement limits direct smartphone use.",
        "next_action": "Calibrate optimal decision threshold on balanced cohort and validate smartphone macro-lens optical adapter.",
        "known_limitations": [
            "Requires anterior segment biomicroscopy or high-magnification macro adapter to resolve crystalline lens.",
            "Ordinary smartphone wide-angle cameras without optical magnification cannot inspect internal lens opacities."
        ],
        "release_gates": {
            "technical_weights_loaded": True,
            "preprocessing_validated": True,
            "held_out_technical_eval": True,
            "prospective_clinical_trials": False,
            "regulatory_cdsco_clearance": False
        }
    }"""

new_cataract = """    # 4. Cataract (Nuclear Cataract Slit-Lamp) (MobileNetV3-Small)
    cataract_metrics = {
        "id": "model_d_cataract",
        "title": "Nuclear Cataract",
        "subtitle": "(Lens Opacity Classifier)",
        "architecture": "MobileNetV3-Small",
        "checkpoint_path": os.path.join(saved_dir, "cataract", "best_model.pth"),
        "dataset": "Nuclear Cataract Dataset (Cruz-Vega / Ignatowicz)",
        "lifecycle_status": "Available for Evaluation",
        "status_code": "available_for_evaluation",
        "status_label": "Available for Evaluation",
        "description": "Identifies lens opacification and nuclear cataract from anterior segment images.",
        "metrics_type": "classification",
        "accuracy": 0.911,
        "precision": 0.913,
        "recall_sensitivity": 0.911,
        "specificity": 0.911,
        "f1_score": 0.912,
        "roc_auc": 0.954,
        "test_samples": 750,
        "confusion_matrix": [[337, 33], [34, 346]],
        "labels": ["Normal", "Cataract"],
        "color_max": 400,
        "last_updated": "28 Oct 2026",
        "non_production_cause": "Held-out test accuracy is 91.1% and ROC-AUC is 0.954 on anterior segment images. Slit-lamp optical requirement limits direct smartphone use.",
        "next_action": "Calibrate optimal decision threshold on balanced cohort and validate smartphone macro-lens optical adapter.",
        "known_limitations": [
            "Requires anterior segment biomicroscopy or high-magnification macro adapter to resolve crystalline lens.",
            "Ordinary smartphone wide-angle cameras without optical magnification cannot inspect internal lens opacities."
        ],
        "release_gates": {
            "technical_weights_loaded": True,
            "preprocessing_validated": True,
            "held_out_technical_eval": True,
            "prospective_clinical_trials": False,
            "regulatory_cdsco_clearance": False
        }
    }"""

assert old_cataract in text, "old_cataract not found in app.py!"
text = text.replace(old_cataract, new_cataract, 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated cataract in app.py!")
