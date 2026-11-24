import pytest
from src.inference.clinical_analytics import compute_anemia_clinical_decision

def test_extreme_low_hb_bounds():
    # Model predictions should constrain 95% CI lower bound to physiological minimum
    decision = compute_anemia_clinical_decision(hb_val=2.5, age_years=30, clinical_sex="male")
    assert decision["confidence_interval_95"]["lower_g_dl"] >= 3.5
    assert decision["who_stage"] == "severe_anemia"

def test_extreme_high_hb_bounds():
    # Upper bound should not exceed 20.0 g/dL
    decision = compute_anemia_clinical_decision(hb_val=22.0, age_years=30, clinical_sex="female")
    assert decision["confidence_interval_95"]["upper_g_dl"] <= 20.0
    assert decision["who_stage"] == "normal_non_anemic"
