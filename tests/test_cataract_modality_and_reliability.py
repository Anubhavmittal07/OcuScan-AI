"""
tests/test_cataract_modality_and_reliability.py
------------------------------------------------
Comprehensive test suite verifying the Cataract Modality Gate & Prediction Reliability:
1. Valid normal slit-lamp image (LOCS III Grade 1 / Non-Cataractous).
2. Valid cataract slit-lamp image (Nuclear Cataract opacification).
3. Ordinary webcam/external-eye image (Rejects false Grade 4; returns clear Inconclusive).
4. Missing/ambiguous modality metadata handling (Content-based optical check; never assumes slit-lamp).
5. Poor-quality or incorrectly framed image (Blur / low resolution gating).
6. Regression tests ensuring Anemia, SLID, Jaundice, Stye, and reports remain intact.
"""

import os
import sys
import pytest
from PIL import Image, ImageFilter
from fastapi.testclient import TestClient

WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

from app import app
from src.inference.unified_service import UnifiedInferenceService
from src.preprocessing.image_quality import validate_cataract_imaging_requirements
from src.inference.pdf_report import build_screening_report_pdf


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def service():
    return UnifiedInferenceService()


def test_1_valid_normal_slit_lamp(service):
    """Scenario 1: Valid normal slit-lamp image reaches model, predicts clear lens, and generates Grad-CAM."""
    path = "data/raw/catscreen/Data2025-main/Clean/Clean images/1016DRPSL (1).jpg"
    assert os.path.exists(path), f"CatScreen normal reference image not found at {path}"
    
    img = Image.open(path)
    res = service.predict_cataract(img, capture_source="upload")
    
    assert res.status == "available_research_only", f"Expected available_research_only, got {res.status}"
    assert res.prediction is not None and len(res.prediction) > 0
    p = res.prediction[0]
    
    assert p["predicted_class"] == "normal_clear_lens", f"Expected normal_clear_lens, got {p['predicted_class']}"
    assert p["locs_grade_estimate"] == 1
    assert p["clinical_decision"]["is_cataract"] is False
    assert p["confidence"] >= 0.50
    
    # Verify Grad-CAM attribution is generated for active permitted inference
    assert p.get("attribution") is not None
    assert p["attribution"].get("status") in ("available", "ready") or "overlay_b64" in p["attribution"]
    assert res.attribution is not None


def test_2_valid_cataract_slit_lamp(service):
    """Scenario 2: Valid cataract slit-lamp image reaches model, detects cataract, and estimates LOCS grade."""
    path = "data/raw/catscreen/Data2025-main/Clean/Clean images/1069DLPSL (1).jpg"
    assert os.path.exists(path), f"CatScreen cataract reference image not found at {path}"
    
    img = Image.open(path)
    res = service.predict_cataract(img, capture_source="upload")
    
    assert res.status == "available_research_only"
    assert res.prediction is not None and len(res.prediction) > 0
    p = res.prediction[0]
    
    assert p["predicted_class"] == "nuclear_cataract", f"Expected nuclear_cataract, got {p['predicted_class']}"
    assert p["locs_grade_estimate"] in (2, 3, 4, 5, 6)
    assert p["clinical_decision"]["is_cataract"] is True
    assert p["confidence"] >= 0.50
    assert p.get("attribution") is not None


def test_3_ordinary_eye_and_webcam_rejected_no_false_cataract(service):
    """Scenario 3: Ordinary eye images (even if 4032x3024) and webcams must NOT receive false cataract predictions."""
    path = "test_images/demo/normal.jpeg"
    assert os.path.exists(path)
    
    # 3a. Ordinary diffuse ambient photo resized to 4032x3024
    img_phone = Image.open(path).resize((4032, 3024))
    img_phone.filename = "my_eye_photo.jpg"
    res_phone = service.predict_cataract(img_phone, capture_source="upload")
    
    assert res_phone.status == "unsupported_image", f"Expected unsupported_image, got {res_phone.status}"
    p_phone = res_phone.prediction[0]
    assert p_phone["predicted_class"] == "inconclusive_modality"
    assert p_phone["confidence"] == 0.0
    assert p_phone["locs_grade_estimate"] is None
    assert p_phone["clinical_decision"]["is_cataract"] is None
    assert "Inconclusive" in p_phone["clinical_decision"]["finding_en"]
    # Verify no Grad-CAM attribution is generated for blocked prediction
    assert p_phone.get("attribution") is None
    assert res_phone.attribution is None

    # 3b. Ordinary webcam capture
    res_webcam = service.predict_cataract(img_phone, capture_source="webcam", experimental_override=False)
    assert res_webcam.status == "blocked_domain_validation"
    assert res_webcam.prediction is None or res_webcam.prediction[0]["predicted_class"] == "inconclusive_modality"
    assert res_webcam.attribution is None


def test_4_missing_or_ambiguous_modality_metadata(service):
    """Scenario 4: Missing metadata is handled explicitly via content verification, never blindly assumed slit-lamp."""
    # 4a. Ambient eye image without modality metadata -> Inconclusive
    img_ambient = Image.open("test_images/demo/normal.jpeg")
    img_ambient.filename = "case_101.jpg"
    res_amb = service.predict_cataract(img_ambient, capture_source="upload", modality=None)
    assert res_amb.status == "unsupported_image"
    assert res_amb.prediction[0]["predicted_class"] == "inconclusive_modality"
    
    # 4b. Genuine Topcon slit-lamp image renamed with generic filename -> Optically recognized and permitted
    topcon_path = "Nuclear Cataract Dataset/35/DER/IM000000.JPG"
    assert os.path.exists(topcon_path)
    img_topcon = Image.open(topcon_path)
    img_topcon.filename = "generic_case_77.jpg"  # no "slit" or "locs" in filename!
    res_topcon = service.predict_cataract(img_topcon, capture_source="upload", modality=None)
    assert res_topcon.status == "available_research_only"
    assert res_topcon.prediction[0]["predicted_class"] in ("normal_clear_lens", "nuclear_cataract")
    assert res_topcon.prediction[0].get("attribution") is not None


def test_5_poor_quality_and_framing(service):
    """Scenario 5: Poor quality (blur) or low resolution images must be rejected by the quality gate."""
    path = "data/raw/catscreen/Data2025-main/Clean/Clean images/1016DRPSL (1).jpg"
    img = Image.open(path)
    
    # 5a. Artificially blurry image
    blurry_img = img.filter(ImageFilter.GaussianBlur(radius=10))
    blurry_img.filename = "1016DRPSL.jpg"
    res_blur = service.predict_cataract(blurry_img, capture_source="upload")
    assert res_blur.status == "unsupported_image"
    assert res_blur.prediction[0]["predicted_class"] == "inconclusive_modality"
    assert any("blurry" in w.lower() for w in res_blur.warnings)
    
    # 5b. Extremely low resolution image (< 180x180)
    tiny_img = img.resize((120, 90))
    tiny_img.filename = "1016DRPSL.jpg"
    res_tiny = service.predict_cataract(tiny_img, capture_source="upload")
    assert res_tiny.status == "unsupported_image"
    assert res_tiny.prediction[0]["predicted_class"] == "inconclusive_modality"
    assert any("dimensions" in w.lower() or "unsuitable" in w.lower() for w in res_tiny.warnings)


def test_6_regression_other_models_and_pdf_report(service, client):
    """Scenario 6: Regression tests confirming Anemia, SLID, Jaundice, Stye, and PDF report generation remain unaffected."""
    test_img_path = "test_images/demo/normal.jpeg"
    with open(test_img_path, "rb") as f:
        # Test unified 5-target screening via API
        response = client.post(
            "/api/analyze",
            data={"module": "unified", "capture_source": "upload"},
            files={"images": ("normal.jpeg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    data = response.json()
    
    # Anemia, SLID, Jaundice, Stye must produce active findings
    assert "anemia" in data
    assert "slid" in data
    assert "jaundice" in data
    assert "stye" in data
    assert "cataract" in data
    
    # For ordinary normal.jpeg, cataract must be inconclusive_modality
    cat_out = data["cataract"]["prediction"][0]
    assert cat_out["predicted_class"] == "inconclusive_modality"
    assert data["cataract"]["attribution"] is None  # No stale heatmap for blocked cataract
    
    # Stye and SLID must have evaluated
    assert data["stye"]["prediction"] is not None
    assert data["slid"]["prediction"] is not None
    
    # PDF generation must succeed
    pdf_bytes = build_screening_report_pdf(data)
    assert len(pdf_bytes) > 1000
    assert pdf_bytes.startswith(b"%PDF")
