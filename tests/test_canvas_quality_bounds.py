import pytest
from PIL import Image
from src.preprocessing.image_quality import calculate_image_quality

def test_neutral_gray_canvas():
    gray_img = Image.new("RGB", (224, 224), color=(128, 128, 128))
    metrics = calculate_image_quality(gray_img)
    assert metrics["brightness"] == 128.0
    assert metrics["contrast"] == 0.0
    assert metrics["sharpness"] == 0.0
