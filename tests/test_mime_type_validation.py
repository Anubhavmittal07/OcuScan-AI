import pytest
from src.config import settings

def test_allowed_mime_types():
    assert "image/jpeg" in settings.ALLOWED_MIME_TYPES
    assert "image/png" in settings.ALLOWED_MIME_TYPES
    assert "application/pdf" not in settings.ALLOWED_MIME_TYPES
