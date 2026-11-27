import pytest
from PIL import Image
from src.preprocessing.image_quality import calculate_image_quality

def test_contrast_and_sharpness_non_negative():
    img = Image.new("RGB", (224, 224), color=(60, 120, 180))
    res = calculate_image_quality(img)
    assert res["contrast"] >= 0.0
    assert res["sharpness"] >= 0.0
