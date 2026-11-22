import pytest
from PIL import Image

def validate_minimum_ocular_dimensions(img: Image.Image, min_dim: int = 128) -> bool:
    width, height = img.size
    return width >= min_dim and height >= min_dim

def test_valid_image_dimensions():
    img = Image.new("RGB", (224, 224))
    assert validate_minimum_ocular_dimensions(img) is True

def test_substandard_image_dimensions():
    img = Image.new("RGB", (64, 64))
    assert validate_minimum_ocular_dimensions(img) is False
