import pytest
from PIL import Image
from src.preprocessing.image_quality import resize_and_pad

def test_resize_and_pad_preserves_target_resolution():
    # Asymmetric input must be padded cleanly into 224x224 square
    img = Image.new("RGB", (300, 150), color=(100, 150, 200))
    resized = resize_and_pad(img, target_size=(224, 224))
    assert resized.size == (224, 224)
