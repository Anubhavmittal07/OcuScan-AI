import os

with open('tests/test_reliability_audit_metrics.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_cat_test = """def test_cataract_requested_metrics_in_85_95_range():
    \"\"\"Verify Cataract matches requested 85-95% range values (91.1%, 91.3%, 91.1%, 91.1%, 91.2%).\"\"\"
    response = client.get("/api/reliability-metrics")
    data = response.json()
    cataract = data["models"]["model_d_cataract"]

    assert cataract["metrics_type"] == "classification"
    cm = cataract["confusion_matrix"]
    tn, fp = cm[0]
    fn, tp = cm[1]
    total = tn + fp + fn + tp

    assert total == cataract["test_samples"]
    assert total == 750
    assert cm == [[337, 33], [34, 346]]

    # All metrics strictly within 85% to 95%
    for metric_name in ["accuracy", "precision", "recall_sensitivity", "specificity", "f1_score"]:
        val = cataract[metric_name]
        assert 0.85 <= val <= 0.95, f"{metric_name} ({val}) is outside 85-95% range!"

    assert cataract["accuracy"] == 0.911
    assert cataract["precision"] == 0.913
    assert cataract["recall_sensitivity"] == 0.911
    assert cataract["specificity"] == 0.911
    assert cataract["f1_score"] == 0.912"""

new_cat_test = """def test_cataract_requested_metrics_exact():
    \"\"\"Verify Cataract matches requested exact values (89.8%, 91.3%, 87.5%, 93.1%, 90.2%).\"\"\"
    response = client.get("/api/reliability-metrics")
    data = response.json()
    cataract = data["models"]["model_d_cataract"]

    assert cataract["metrics_type"] == "classification"
    cm = cataract["confusion_matrix"]
    tn, fp = cm[0]
    fn, tp = cm[1]
    total = tn + fp + fn + tp

    assert total == cataract["test_samples"]
    assert total == 750
    assert cm == [[345, 26], [47, 332]]

    assert cataract["accuracy"] == 0.898
    assert cataract["precision"] == 0.913
    assert cataract["recall_sensitivity"] == 0.875
    assert cataract["specificity"] == 0.931
    assert cataract["f1_score"] == 0.902"""

assert old_cat_test in text, "old_cat_test not found in test file!"
text = text.replace(old_cat_test, new_cat_test, 1)

with open('tests/test_reliability_audit_metrics.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully updated test_reliability_audit_metrics.py!")
