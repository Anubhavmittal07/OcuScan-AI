import pytest
from src.inference.clinical_analytics import compute_anemia_clinical_decision

def test_pediatric_population_flag():
    decision = compute_anemia_clinical_decision(hb_val=12.5, age_years=10, clinical_sex="male")
    assert decision["population_validation"]["is_validated_population"] is False
    assert decision["population_validation"]["status"] == "outside_validated_population"
    assert decision["population_validation"]["reason"] == "pediatric_under_18"

def test_adult_female_normal_hb():
    decision = compute_anemia_clinical_decision(hb_val=13.0, age_years=28, clinical_sex="female")
    assert decision["who_stage"] == "normal_non_anemic"
    assert decision["population_validation"]["is_validated_population"] is True

def test_adult_male_mild_anemia():
    decision = compute_anemia_clinical_decision(hb_val=11.8, age_years=35, clinical_sex="male")
    assert decision["who_stage"] == "mild_anemia"
    assert decision["population_validation"]["is_validated_population"] is True

def test_geriatric_boundary_flag():
    decision = compute_anemia_clinical_decision(hb_val=12.2, age_years=92, clinical_sex="female")
    assert decision["population_validation"]["is_validated_population"] is False
    assert decision["population_validation"]["status"] == "outside_validated_population"
    assert decision["population_validation"]["reason"] == "geriatric_over_88"
