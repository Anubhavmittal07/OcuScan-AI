import pytest
from src.preprocessing.image_quality import safe_load_image

def test_load_nonexistent_image_gracefully():
    # Attempting to load a file that does not exist should return None without crashing
    res = safe_load_image("nonexistent_directory/fake_ocular_capture.jpg")
    assert res is None
