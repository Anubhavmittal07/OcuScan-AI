import pytest
from src.inference.copilot import sanitize_input, is_blocked_topic

def test_sanitize_file_paths():
    sample = r"Check file at C:\Users\JohnDoe\Desktop\patient.jpg please"
    sanitized = sanitize_input(sample)
    assert "JohnDoe" not in sanitized
    assert "[REDACTED_PATH]" in sanitized

def test_sanitize_hemoglobin_values():
    sample = "Patient has 9.4 g/dL and needs review"
    sanitized = sanitize_input(sample)
    assert "9.4" not in sanitized
    assert "[REDACTED_HB_VALUE]" in sanitized

def test_sanitize_email_addresses():
    sample = "Contact clinician at doctor@hospital.org immediately"
    sanitized = sanitize_input(sample)
    assert "doctor@hospital.org" not in sanitized
    assert "[REDACTED_EMAIL]" in sanitized

def test_blocked_medical_advice_topics():
    assert is_blocked_topic("What is this disease?") is True
    assert is_blocked_topic("Please diagnose this patient") is True
    assert is_blocked_topic("Should the patient take antibiotics?") is True
    assert is_blocked_topic("How does ResNet50 extract features?") is False
