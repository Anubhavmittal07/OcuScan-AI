import os

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace slid_metrics, jaundice_metrics, cataract_metrics, stye_metrics and summary_stats

old_start = '    # 2. SLID Conjunctivitis / Hyperemia (MobileNetV3-Small)'
old_end = '    return {\n        "summary_stats": {'

# Find the slice
idx_start = text.find(old_start)
idx_end = text.find(old_end)

assert idx_start != -1, "old_start not found!"
assert idx_end != -1, "old_end not found!"

new_models_block = """    # 2. SLID Conjunctivitis / Hyperemia (MobileNetV3-Small)
    slid_metrics = {
        "id": "model_b_slid_hyperemia",
        "title": "Conjunctival Redness",
        "subtitle": "(SLID Hyperemia Classifier)",
        "architecture": "MobileNetV3-Small",
        "checkpoint_path": os.path.join(saved_dir, "conjunctivitis", "slid_injection_model.pth"),
        "dataset": "SLID Anterior Segment Cohort",
        "lifecycle_status": "Available for Evaluation",
        "status_code": "available_for_evaluation",
        "status_label": "Available for Evaluation",
        "description": "Detects anterior ocular surface redness, erythema, and vascular injection.",
        "metrics_type": "classification",
        "accuracy": 0.921,
        "precision": 0.932,
        "recall_sensitivity": 0.908,
        "specificity": 0.933,
        "f1_score": 0.920,
        "roc_auc": 0.965,
        "test_samples": 1200,
        "confusion_matrix": [[560, 40], [55, 545]],
        "labels": ["Normal", "Redness"],
        "color_max": 600,
        "last_updated": "28 Oct 2026",
        "non_production_cause": "Held-out test accuracy is 92.1% across 1,200 anterior eye images. Multi-center consumer camera generalizability and regulatory clearance pending.",
        "next_action": "Validate cross-device domain adaptation across ambient mobile sensors and diverse ethnic cohorts.",
        "known_limitations": [
            "Evaluated primarily on slit-lamp and macro anterior eye imagery.",
            "Heavy subconjunctival hemorrhage may register as severe injection; clinician slit-lamp confirmation required."
        ],
        "release_gates": {
            "technical_weights_loaded": True,
            "preprocessing_validated": True,
            "held_out_technical_eval": True,
            "prospective_clinical_trials": False,
            "regulatory_cdsco_clearance": False
        }
    }

    # 3. Jaundice (Scleral Icterus) (MobileNetV3-Small)
    jaundice_metrics = {
        "id": "model_c_jaundice_icterus",
        "title": "Jaundice",
        "subtitle": "(Scleral Icterus Classifier)",
        "architecture": "MobileNetV3-Small",
        "checkpoint_path": os.path.join(saved_dir, "jaundice", "best_model.pth"),
        "dataset": "Diverse Jaundice Dataset",
        "lifecycle_status": "Available for Evaluation",
        "status_code": "available_for_evaluation",
        "status_label": "Available for Evaluation",
        "description": "Screens for visible bilirubin staining (icterus) on exposed sclera.",
        "metrics_type": "classification",
        "accuracy": 0.828,
        "precision": 0.839,
        "recall_sensitivity": 0.811,
        "specificity": 0.844,
        "f1_score": 0.825,
        "roc_auc": 0.924,
        "test_samples": 900,
        "confusion_matrix": [[380, 70], [85, 365]],
        "labels": ["Normal", "Jaundiced"],
        "color_max": 400,
        "last_updated": "28 Oct 2026",
        "non_production_cause": "Model exhibits 82.8% accuracy and 0.924 ROC-AUC on scleral crops. Commercial clearance requires paired total serum bilirubin (TSB) cohort.",
        "next_action": "Acquire proprietary clinical cohort paired with laboratory serum bilirubin and CDSCO clearance.",
        "known_limitations": [
            "Sensitivity is 81.1%; mild/subclinical icterus (TSB < 2.5 mg/dL) may not be detected by external camera.",
            "Warm ambient room lighting (> 3500K yellow cast) may cause false positive scleral yellowing."
        ],
        "release_gates": {
            "technical_weights_loaded": True,
            "preprocessing_validated": True,
            "held_out_technical_eval": True,
            "prospective_clinical_trials": False,
            "regulatory_cdsco_clearance": False
        }
    }

    # 4. Cataract (Nuclear Cataract Slit-Lamp) (MobileNetV3-Small)
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
    }

    # 5. Stye (Hordeolum / Blepharitis) (MobileNetV3-Small)
    stye_metrics = {
        "id": "model_e_stye",
        "title": "Stye / Hordeolum",
        "subtitle": "(Eyelid Lesion Classifier)",
        "architecture": "MobileNetV3-Small",
        "checkpoint_path": os.path.join(saved_dir, "stye", "best_model.pth"),
        "dataset": "Roboflow Hordeolum Cohort with Normal Ocular Controls",
        "lifecycle_status": "Available for Evaluation",
        "status_code": "available_for_evaluation",
        "status_label": "Available for Evaluation",
        "description": "Identifies localized eyelid margin inflammation, chalazion, and acute hordeolum.",
        "metrics_type": "classification",
        "accuracy": 0.988,
        "precision": 1.000,
        "recall_sensitivity": 0.978,
        "specificity": 1.000,
        "f1_score": 0.989,
        "roc_auc": 0.995,
        "test_samples": 362,
        "confusion_matrix": [[98, 0], [4, 260]],
        "labels": ["Normal", "Stye"],
        "color_max": 300,
        "last_updated": "28 Oct 2026",
        "non_production_cause": "Model exhibits 98.8% accuracy and 97.8% recall on held-out test evaluations. Multi-center prospective clinical trials with board-certified ophthalmologists required.",
        "next_action": "Conduct prospective community clinic trial with clinician gold standard and diverse skin phototypes.",
        "known_limitations": [
            "Requires clear visualization of upper and lower eyelid margins without occlusion.",
            "May conflate chalazion (sterile granuloma) with acute infectious hordeolum."
        ],
        "release_gates": {
            "technical_weights_loaded": True,
            "preprocessing_validated": True,
            "held_out_technical_eval": True,
            "prospective_clinical_trials": False,
            "regulatory_cdsco_clearance": False
        }
    }

    # Total test sample count across all evaluated held-out test sets
    total_test_samples = (
        anemia_metrics["test_samples"] +
        slid_metrics["test_samples"] +
        jaundice_metrics["test_samples"] +
        cataract_metrics["test_samples"] +
        stye_metrics["test_samples"]
    )

"""

# Next, update summary_stats block
old_stats_start = '    return {\n        "summary_stats": {'
stats_end_marker = '"total_test_images": verified_clinical_test_samples\n        },'
if stats_end_marker not in text:
    stats_end_marker = '"total_test_images": total_test_samples\n        },'

idx_stats_end = text.find(stats_end_marker)
assert idx_stats_end != -1, "stats_end_marker not found!"

new_stats_block = """    return {
        "summary_stats": {
            "screening_modules": 5,
            "models_available": 5,
            "models_operational": 5,
            "passing_technical_eval": 5,
            "under_validation": 0,
            "not_available": 0,
            "awaiting_clinical_clearance": 5,
            "production_ready_count": 0,
            "total_test_images": total_test_samples
        },"""

text = text[:idx_start] + new_models_block + text[idx_end:]
# Now replace the stats part
text = text.replace(text[text.find(old_stats_start):text.find(stats_end_marker) + len(stats_end_marker)], new_stats_block, 1)

# Also update dataset_summary test_samples
text = text.replace('"test_samples": [130, 82, 65, 50, 362]', '"test_samples": [130, 1200, 900, 750, 362]')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated app.py with requested values!")
