import pytest
from src.inference.clinical_analytics import compute_anemia_clinical_decision

def test_pregnancy_defaults_to_false():
    decision = compute_anemia_clinical_decision(hb_val=12.5, age_years=25, clinical_sex="female")
    assert decision["clinical_reference_group"] == "Non-Pregnant Females (≥15 years, WHO 2024)"
    assert decision["norm_threshold_g_dl"] == 12.0

def test_explicit_pregnancy_trimester():
    decision = compute_anemia_clinical_decision(
        hb_val=10.2, age_years=25, clinical_sex="female", is_pregnant=True, pregnancy_trimester=2
    )
    assert "Pregnant Females (2nd Trimester" in decision["clinical_reference_group"]
    assert decision["norm_threshold_g_dl"] == 10.5
