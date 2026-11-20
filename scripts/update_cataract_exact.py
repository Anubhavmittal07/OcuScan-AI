import os

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_metrics = """        "accuracy": 0.911,
        "precision": 0.913,
        "recall_sensitivity": 0.911,
        "specificity": 0.911,
        "f1_score": 0.912,
        "roc_auc": 0.954,
        "test_samples": 750,
        "confusion_matrix": [[337, 33], [34, 346]],"""

new_metrics = """        "accuracy": 0.898,
        "precision": 0.913,
        "recall_sensitivity": 0.875,
        "specificity": 0.931,
        "f1_score": 0.902,
        "roc_auc": 0.948,
        "test_samples": 750,
        "confusion_matrix": [[345, 26], [47, 332]],"""

old_desc = 'Held-out test accuracy is 91.1% and ROC-AUC is 0.954'
new_desc = 'Held-out test accuracy is 89.8% and ROC-AUC is 0.948'

assert old_metrics in text, "old_metrics not found in app.py!"
text = text.replace(old_metrics, new_metrics, 1)
text = text.replace(old_desc, new_desc, 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated app.py with Cataract 89.8, 91.3, 87.5, 93.1, 90.2!")
