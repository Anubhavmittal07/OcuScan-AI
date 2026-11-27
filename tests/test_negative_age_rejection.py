import pytest
from pydantic import ValidationError
from app import UserRegisterRequest

def test_negative_age_rejected():
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            full_name="Test Patient",
            phone="1234567890",
            email="patient@test.com",
            age_years=-5
        )

def test_overage_boundary_rejected():
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            full_name="Test Patient",
            phone="1234567890",
            email="patient@test.com",
            age_years=130
        )
