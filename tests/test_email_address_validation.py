import pytest
from src.utils.email_service import validate_email_address

def test_hospital_and_standard_emails():
    assert validate_email_address("lead.optometrist@district-hospital.org") is True
    assert validate_email_address("screener_team@moh.gov.in") is True

def test_malformed_email_rejection():
    assert validate_email_address("not_an_email") is False
    assert validate_email_address("missing-domain@") is False
    assert validate_email_address("@missing-username.com") is False
