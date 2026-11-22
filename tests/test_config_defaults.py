import os
import pytest
from src.config import settings

def test_default_environment():
    assert settings.ENV in ("development", "production", "testing")

def test_allowed_extensions():
    assert ".jpg" in settings.ALLOWED_IMAGE_EXTENSIONS
    assert ".png" in settings.ALLOWED_IMAGE_EXTENSIONS
    assert ".exe" not in settings.ALLOWED_IMAGE_EXTENSIONS

def test_max_upload_size():
    assert settings.MAX_UPLOAD_SIZE_MB > 0
    assert settings.MAX_UPLOAD_SIZE_BYTES == settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

def test_checkpoint_paths_defined():
    assert settings.ANEMIA_CHECKPOINT_PATH is not None
    assert settings.SLID_CHECKPOINT_PATH is not None
