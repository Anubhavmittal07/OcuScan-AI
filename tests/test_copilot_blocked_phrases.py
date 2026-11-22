import pytest
from src.inference.copilot import is_blocked_topic

def test_diagnostic_phrases_blocked():
    blocked = [
        "Please diagnose this patient condition",
        "What is this disease?",
        "Should the patient take antibiotics?",
        "Prescribe a treatment for this patient"
    ]
    for phrase in blocked:
        assert is_blocked_topic(phrase) is True

def test_research_phrases_permitted():
    permitted = [
        "How is the MobileNetV3 architecture structured?",
        "What is the function of the Laplacian filter in image quality?",
        "Explain the formula for Erythema Index",
        "How does Grad-CAM compute activation gradients?"
    ]
    for phrase in permitted:
        assert is_blocked_topic(phrase) is False
