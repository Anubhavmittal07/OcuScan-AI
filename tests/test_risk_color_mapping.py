import pytest
from src.inference.clinical_analytics import compute_anemia_clinical_decision

def test_severe_anemia_color_mapping():
    decision = compute_anemia_clinical_decision(hb_val=6.5, age_years=30, clinical_sex="male")
    assert decision["who_stage"] == "severe_anemia"
    assert decision["risk_color"] == "#ef4444"

def test_mild_anemia_color_mapping():
    decision = compute_anemia_clinical_decision(hb_val=11.5, age_years=30, clinical_sex="male")
    assert decision["who_stage"] == "mild_anemia"
    assert decision["risk_color"] == "#eab308"

def test_normal_non_anemic_color_mapping():
    decision = compute_anemia_clinical_decision(hb_val=14.0, age_years=30, clinical_sex="male")
    assert decision["who_stage"] == "normal_non_anemic"
    assert decision["risk_color"] == "#10b981"
