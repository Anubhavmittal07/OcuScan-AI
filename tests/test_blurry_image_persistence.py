import io
import os
import sys
import numpy as np
from PIL import Image, ImageFilter
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from src.database.session import sanitize_for_json, safe_json_dumps

client = TestClient(app)

def test_sanitize_for_json_with_numpy_primitives():
    """Verify sanitize_for_json converts all numpy primitives to native python types."""
    data = {
        "bool_val": np.bool_(True),
        "int_val": np.int64(42),
        "float_val": np.float32(8.18),
        "arr_val": np.array([1.0, 2.0, 3.0]),
        "nested": {
            "is_blurry": np.bool_(False),
            "flags": [np.bool_(True), np.bool_(False)]
        }
    }
    cleaned = sanitize_for_json(data)
    assert type(cleaned["bool_val"]) is bool
    assert type(cleaned["int_val"]) is int
    assert type(cleaned["float_val"]) is float
    assert type(cleaned["arr_val"]) is list
    assert type(cleaned["nested"]["is_blurry"]) is bool
    assert type(cleaned["nested"]["flags"][0]) is bool

    # safe_json_dumps must succeed without error
    serialized = safe_json_dumps(data)
    assert "true" in serialized
    assert "8.18" in serialized

def test_blurry_image_analysis_persistence():
    """Verify an intentionally blurred image (sharpness < 24) saves to the database successfully."""
    # Create an image and apply strong Gaussian blur to ensure laplacian variance < 20
    base_img = Image.new("RGB", (300, 300), color=(140, 70, 60))
    blurred = base_img.filter(ImageFilter.GaussianBlur(radius=8))
    
    buf = io.BytesIO()
    blurred.save(buf, format="JPEG")
    buf.seek(0)

    files = [("images", ("blurry_eye.jpg", buf, "image/jpeg"))]
    resp = client.post(
        "/api/analyze?module=unified&capture_source=upload&age_years=28&clinical_sex=male",
        files=files
    )
    
    # Must NOT fail with 500 or Database persistence failure
    assert resp.status_code == 200, f"Analyze failed with error: {resp.text}"
    result = resp.json()
    assert result.get("session_id") is not None
    assert result.get("status") in ("available_research_only", "processed", "marginal")

    # Verify report endpoint retrieves it cleanly from database
    sid = result["session_id"]
    rep_resp = client.get(f"/api/reports/{sid}")
    assert rep_resp.status_code == 200
    rep_data = rep_resp.json()
    assert rep_data.get("session_id") == sid


def test_quality_check_endpoint_returns_json_safe_primitives():
    """Verify /api/quality-check serializes numpy types cleanly without 500 TypeError."""
    img = Image.new("RGB", (320, 240), color=(120, 140, 160))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"image": ("test_eye.jpg", buf, "image/jpeg")}
    resp = client.post("/api/quality-check", files=files)
    assert resp.status_code == 200, f"Quality check failed with: {resp.text}"
    data = resp.json()
    assert data["is_valid"] is True
    assert "quality" in data
    assert isinstance(data["quality"]["sharpness"], (int, float))
    assert isinstance(data["quality"]["is_blurry"], bool)

