import pytest
import numpy as np
from src.preprocessing.image_quality import calculate_image_quality

def test_uniform_black_image_quality():
    # Pure black image should flag under-exposure
    black_img = np.zeros((224, 224, 3), dtype=np.uint8)
    metrics = calculate_image_quality(black_img)
    assert metrics["passed"] is False
    assert metrics["exposure_status"] == "under_exposed"

def test_uniform_white_image_quality():
    # Pure white image should flag over-exposure
    white_img = np.full((224, 224, 3), 255, dtype=np.uint8)
    metrics = calculate_image_quality(white_img)
    assert metrics["passed"] is False
    assert metrics["exposure_status"] == "over_exposed"

def test_sharpness_calculation_positive():
    rng = np.random.default_rng(42)
    noise_img = rng.integers(50, 200, size=(224, 224, 3), dtype=np.uint8)
    metrics = calculate_image_quality(noise_img)
    assert metrics["sharpness"] > 0
