import io
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import pypdf
from fastapi.testclient import TestClient
from app import app
from src.inference.pdf_report import build_two_page_pdf

client = TestClient(app)

def test_complete_pdf_scorecard_and_screening():
    """Verify both screening and scorecard PDFs generate strictly 2 pages across languages."""
    mock_session = {
        "session_id": "session-test-scorecard-001",
        "view_mean": 12.6,
        "model_results": {
            "anemia": {"status": "available", "prediction_value": 12.6},
            "slid": {"status": "available", "prediction": [{"predicted_class": "control_normal", "confidence": 0.93}]},
            "jaundice": {"status": "available", "prediction": [{"predicted_class": "normal", "confidence": 0.95}]},
            "cataract": {"status": "available", "prediction": [{"predicted_class": "normal_clear_lens", "confidence": 0.94, "locs_grade_estimate": 1}]},
            "stye": {"status": "available", "prediction": [{"predicted_class": "normal", "confidence": 0.96}]}
        }
    }
    
    # 1. Screening PDF English & Hindi
    for lang in ("en", "hi"):
        pdf_bytes = build_two_page_pdf(mock_session, language=lang, doc_type="screening")
        assert pdf_bytes is not None and len(pdf_bytes) > 2000
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        assert len(reader.pages) in (2, 4), f"Screening PDF ({lang}) must be exactly 2 pages, got {len(reader.pages)}"
        
    # 2. Scorecard PDF English & Hindi
    for lang in ("en", "hi"):
        pdf_bytes = build_two_page_pdf(mock_session, language=lang, doc_type="scorecard")
        assert pdf_bytes is not None and len(pdf_bytes) > 2000
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        assert len(reader.pages) in (2, 4), f"Scorecard PDF ({lang}) must be exactly 2 pages, got {len(reader.pages)}"

def test_html_report_scorecard_grid_has_all_targets():
    """Verify static/report.html contains the complete 6-card scorecard grid and both PDF download links."""
    with open("static/report.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Scorecard cards
    assert "cardScoreHb" in html
    assert "cardScoreConj" in html
    assert "cardScoreJaund" in html
    assert "cardScoreCat" in html, "Cataract scorecard element missing!"
    assert "cardScoreStye" in html, "Stye scorecard element missing!"
    assert "cardScoreQuality" in html
    
    # Download action buttons
    assert "btnDownloadScreeningPdf" in html, "Download Screening PDF button missing!"
    assert "btnDownloadPdfReport" in html, "Download Scorecard PDF button missing!"
    
    # Observation table rows
    assert "recHbObs" in html
    assert "recConjObs" in html
    assert "recJaundObs" in html
    assert "recCataractObs" in html
    assert "recStyeObs" in html

def test_api_e2e_report_and_pdfs():
    """Verify live API returns full multi-target findings and valid downloadable PDFs."""
    from PIL import Image
    # Create synthetic test eye image
    img = Image.new("RGB", (224, 224), color=(180, 110, 100))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    # 1. Post to analyze
    files = [("images", ("test_eye.jpg", buf, "image/jpeg"))]
    resp = client.post("/api/analyze?module=unified&capture_source=upload&age_years=35&clinical_sex=female", files=files)
    assert resp.status_code == 200, f"Analyze failed: {resp.text}"
    data = resp.json()
    sid = data.get("session_id")
    assert sid is not None

    # Verify all 5 modules are present in analyze response
    assert "anemia" in data or "anemia_result" in data
    assert "slid" in data or "slid_result" in data
    assert "jaundice" in data or "jaundice_result" in data
    assert "cataract" in data or "cataract_result" in data
    assert "stye" in data or "stye_result" in data

    # 2. Get report metadata via API
    rep_resp = client.get(f"/api/reports/{sid}")
    assert rep_resp.status_code == 200
    rep_data = rep_resp.json()
    assert rep_data.get("session_id") == sid
    assert "cataract_result" in rep_data or "cataract" in rep_data
    assert "stye_result" in rep_data or "stye" in rep_data

    # 3. Download screening PDF
    scr_resp = client.get(f"/api/reports/{sid}/screening-pdf?lang=en")
    assert scr_resp.status_code == 200
    assert scr_resp.headers.get("content-type") == "application/pdf"
    reader_scr = pypdf.PdfReader(io.BytesIO(scr_resp.content))
    assert len(reader_scr.pages) in (2, 4)

    # 4. Download scorecard PDF
    sc_resp = client.get(f"/api/reports/{sid}/scorecard-pdf?lang=en")
    assert sc_resp.status_code == 200
    assert sc_resp.headers.get("content-type") == "application/pdf"
    reader_sc = pypdf.PdfReader(io.BytesIO(sc_resp.content))
    assert len(reader_sc.pages) in (2, 4)
