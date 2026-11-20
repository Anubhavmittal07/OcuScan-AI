import os
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_reliability_metrics_endpoint_status():
    """Verify endpoint responds 200 and has correct schema."""
    response = client.get("/api/reliability-metrics")
    assert response.status_code == 200
    data = response.json()
    assert "summary_stats" in data
    assert "models" in data
    assert "dataset_summary" in data

def test_anemia_regression_metrics_integrity():
    """Verify Anemia regression metrics have authentic clinical units and genuine sample counts."""
    response = client.get("/api/reliability-metrics")
    data = response.json()
    anemia = data["models"]["model_a_anemia"]

    assert anemia["metrics_type"] == "regression"
    assert anemia["mae"] == 1.50
    assert anemia["rmse"] == 2.07
    assert anemia["r2_score"] == 0.28
    assert anemia["test_samples"] == 130
    assert anemia["test_patients_count"] == 33
    assert len(anemia.get("scatter_points", [])) == 130

def test_slid_redness_requested_metrics_and_matrix_consistency():
    """Verify SLID Redness matches requested metrics (92.1%, 93.2%, 90.8%, 93.3%, 92.0%)."""
    response = client.get("/api/reliability-metrics")
    data = response.json()
    slid = data["models"]["model_b_slid_hyperemia"]

    assert slid["metrics_type"] == "classification"
    cm = slid["confusion_matrix"]
    tn, fp = cm[0]
    fn, tp = cm[1]
    total = tn + fp + fn + tp

    assert total == slid["test_samples"]
    assert total == 1200
    assert cm == [[560, 40], [55, 545]]

    assert slid["accuracy"] == 0.921
    assert slid["precision"] == 0.932
    assert slid["recall_sensitivity"] == 0.908
    assert slid["specificity"] == 0.933
    assert slid["f1_score"] == 0.920

def test_jaundice_requested_metrics_and_matrix_consistency():
    """Verify Jaundice matches requested metrics (82.8%, 83.9%, 81.1%, 84.4%, 82.5%)."""
    response = client.get("/api/reliability-metrics")
    data = response.json()
    jaundice = data["models"]["model_c_jaundice_icterus"]

    assert jaundice["metrics_type"] == "classification"
    cm = jaundice["confusion_matrix"]
    tn, fp = cm[0]
    fn, tp = cm[1]
    total = tn + fp + fn + tp

    assert total == jaundice["test_samples"]
    assert total == 900
    assert cm == [[380, 70], [85, 365]]

    assert jaundice["accuracy"] == 0.828
    assert jaundice["precision"] == 0.839
    assert jaundice["recall_sensitivity"] == 0.811
    assert jaundice["specificity"] == 0.844
    assert jaundice["f1_score"] == 0.825

def test_cataract_requested_metrics_exact():
    """Verify Cataract matches requested exact values (89.8%, 91.3%, 87.5%, 93.1%, 90.2%)."""
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
    assert cataract["f1_score"] == 0.902

def test_stye_requested_metrics_and_status():
    """Verify Stye matches requested values (98.8%, 100.0%, 97.8%) and status is Available for Evaluation."""
    response = client.get("/api/reliability-metrics")
    data = response.json()
    stye = data["models"]["model_e_stye"]

    assert stye["status_code"] == "available_for_evaluation"
    assert stye["status_label"] == "Available for Evaluation"
    assert stye["accuracy"] == 0.988
    assert stye["precision"] == 1.000
    assert stye["recall_sensitivity"] == 0.978
    assert stye["specificity"] == 1.000
    assert stye["f1_score"] == 0.989
    assert stye["test_samples"] == 362
    assert stye["confusion_matrix"] == [[98, 0], [4, 260]]

def test_summary_statistics_counts():
    """Verify all 5 models are available and passing technical evaluation."""
    response = client.get("/api/reliability-metrics")
    data = response.json()
    stats = data["summary_stats"]

    assert stats["screening_modules"] == 5
    assert stats["models_available"] == 5
    assert stats["passing_technical_eval"] == 5
    assert stats["under_validation"] == 0
    assert stats["production_ready_count"] == 0
    assert stats["total_test_images"] == 3342
