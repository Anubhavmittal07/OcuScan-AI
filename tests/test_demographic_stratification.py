import pytest
from src.inference.personalized_ai import get_demographic_hb_thresholds

def test_pediatric_thresholds():
    thresholds = get_demographic_hb_thresholds(age=8, sex="male")
    assert thresholds["mild"] == 11.0
    assert thresholds["category"] == "Pediatric (<12y)"

def test_adult_female_thresholds():
    thresholds = get_demographic_hb_thresholds(age=28, sex="female")
    assert thresholds["mild"] == 12.0
    assert thresholds["category"] == "Adult Female"

def test_adult_male_thresholds():
    thresholds = get_demographic_hb_thresholds(age=35, sex="male")
    assert thresholds["mild"] == 13.0
    assert thresholds["category"] == "Adult Male"

def test_geriatric_thresholds():
    thresholds = get_demographic_hb_thresholds(age=72, sex="female")
    assert thresholds["category"] == "Geriatric (>65y)"
