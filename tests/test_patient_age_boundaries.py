import pytest
from src.inference.clinical_analytics import compute_anemia_clinical_decision

def test_pediatric_under_18_warning():
    decision = compute_anemia_clinical_decision(hb_val=12.0, age_years=12, clinical_sex="male")
    assert decision["population_validation"]["is_validated_population"] is False
    assert decision["population_validation"]["reason"] == "pediatric_under_18"

def test_adult_within_validated_cohort():
    decision = compute_anemia_clinical_decision(hb_val=13.5, age_years=35, clinical_sex="male")
    assert decision["population_validation"]["is_validated_population"] is True
