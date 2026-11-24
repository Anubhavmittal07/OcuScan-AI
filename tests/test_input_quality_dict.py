import pytest
from PIL import Image
from src.preprocessing.image_quality import calculate_image_quality

def test_image_quality_dictionary_types():
    img = Image.new("RGB", (224, 224), color=(100, 150, 200))
    res = calculate_image_quality(img)
    assert isinstance(res["brightness"], float)
    assert isinstance(res["contrast"], float)
    assert isinstance(res["sharpness"], float)
