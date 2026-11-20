import pytest
import numpy as np
from PIL import Image
from src.preprocessing.image_quality import calculate_image_quality

def test_uniform_black_image_quality():
    # Pure black PIL image should have 0 brightness and 0 contrast
    black_img = Image.new("RGB", (224, 224), color=(0, 0, 0))
    metrics = calculate_image_quality(black_img)
    assert metrics["brightness"] == 0.0
    assert metrics["contrast"] == 0.0
    assert metrics["sharpness"] == 0.0

def test_uniform_white_image_quality():
    # Pure white PIL image should have 255 brightness and 0 contrast
    white_img = Image.new("RGB", (224, 224), color=(255, 255, 255))
    metrics = calculate_image_quality(white_img)
    assert metrics["brightness"] == 255.0
    assert metrics["contrast"] == 0.0
    assert metrics["sharpness"] == 0.0

def test_sharpness_calculation_positive():
    rng = np.random.default_rng(42)
    noise_arr = rng.integers(50, 200, size=(224, 224, 3), dtype=np.uint8)
    noise_img = Image.fromarray(noise_arr)
    metrics = calculate_image_quality(noise_img)
    assert metrics["sharpness"] > 0
    assert 0 < metrics["brightness"] < 255
