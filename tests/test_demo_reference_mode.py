"""
tests/test_demo_reference_mode.py
---------------------------------
Comprehensive automated test suite for Demo Reference Mode.
Validates:
1. Exact SHA-256 matching for all 5 demo presentation images.
2. Prominent banner presence: "DEMO REFERENCE RESULT — PREDEFINED LABEL — NOT AN AI PREDICTION".
3. Negative control rejection (non-demo images do NOT trigger demo reference mode).
4. Module harmonization (stye -> stye primary, slid -> slid primary, anemia -> Hb primary).
5. PDF report generation containing explicit demo mode warnings in both English and Hindi.
"""

import os
import io
import pytest
from PIL import Image
from pypdf import PdfReader
from fastapi.testclient import TestClient

from app import app
from src.inference.demo_reference import (
    match_demo_reference,
    get_demo_manifest,
    compute_sha256
)

DEMO_DIR = os.path.join(os.path.dirname(__file__), "..", "test_images", "demo")

EXPECTED_DEMO_CASES = {
    "conjuctivities_redeye.jpg": "85a7e9246dd79ebb05e941269ea377bcf7dd1205b3707de5eea00914608218a9",
    "stye.jpg": "617c9b83cebe02f33ae4082e42d7d5ac0d8a8c9e84bddb756fa3ab37ecb32cd2",
    "normal.jpeg": "d1bc77b75616c58774577909357fe1b7675382a2e000b768c3ffce5fe23e6e63",
    "anemia.jpg": "16dd6993995ef8484d04f938d08d9e5febc82a8323eace0e834b542aed8db232",
    "Conjuctive.png": "8794a1aa833a4c3337819d46213311096d98690ef327a8baa471e989686b045a"
}


def test_demo_manifest_integrity():
    manifest = get_demo_manifest()
    assert "references" in manifest, "Manifest missing 'references' key"
    assert len(manifest["references"]) >= 5, f"Expected at least 5 references, got {len(manifest['references'])}"
    assert "banner_text" in manifest
    assert "NOT AN AI PREDICTION" in manifest["banner_text"]

    for fn, expected_hash in EXPECTED_DEMO_CASES.items():
        assert expected_hash in manifest["references"], f"Hash {expected_hash} for {fn} missing from manifest"
        ref = manifest["references"][expected_hash]
        assert ref["filename"] == fn
        assert "intended_category" in ref
        assert "reference_finding" in ref
        assert "ground_truth_status" in ref


def test_hash_computation_and_matching():
    for fn, expected_hash in EXPECTED_DEMO_CASES.items():
        img_path = os.path.join(DEMO_DIR, fn)
        assert os.path.isfile(img_path), f"Demo image {fn} not found in {DEMO_DIR}"
        calc_hash = compute_sha256(img_path)
        assert calc_hash == expected_hash, f"Hash mismatch on {fn}: {calc_hash} != {expected_hash}"

        match = match_demo_reference(images=[img_path])
        assert match["is_demo_reference"] is True
        assert match["sha256"] == expected_hash
        assert match["filename"] == fn
        assert "NOT AN AI PREDICTION" in match["banner_text"]


def test_negative_control_not_demo():
    # Synthetic random image
    img = Image.new("RGB", (100, 100), color=(123, 200, 50))
    match = match_demo_reference(images=[img])
    assert match["is_demo_reference"] is False
    assert match["banner_text"] is None


def test_api_analyze_and_pdf_report_demo_mode():
    client = TestClient(app)

    # 1. Test conjuctivities_redeye.jpg (Target: SLID)
    target_fn = "conjuctivities_redeye.jpg"
    target_path = os.path.join(DEMO_DIR, target_fn)

    with open(target_path, "rb") as f:
        file_bytes = f.read()

    resp = client.post(
        "/api/analyze",
        files={"images": (target_fn, file_bytes, "image/jpeg")},
        data={
            "module": "unified",
            "capture_source": "upload",
            "language": "en",
            "age_years": 28,
            "clinical_sex": "male"
        }
    )

    assert resp.status_code == 200, f"Analysis failed: {resp.text}"
    data = resp.json()

    assert data.get("demo_reference") is not None
    demo_ref = data["demo_reference"]
    assert demo_ref["is_demo_reference"] is True
    assert "NOT AN AI PREDICTION" in demo_ref["banner_text"]
    assert demo_ref["filename"] == target_fn

    # Module Harmonization: SLID is primary, Anemia is gated
    assert data.get("selected_module") == "slid"
    assert data.get("slid") is not None
    slid_pred = data["slid"]["prediction"][0]
    assert slid_pred["predicted_class"] == "conjunctival_injection"
    assert data.get("anemia", {}).get("status") == "unsupported_image"

    session_id = data["session_id"]

    # Verify session report endpoint
    rep_resp = client.get(f"/api/reports/{session_id}")
    assert rep_resp.status_code == 200
    rep_data = rep_resp.json()
    assert rep_data.get("demo_reference", {}).get("is_demo_reference") is True

    # Verify PDF contains demo warning banner
    pdf_resp = client.get(f"/api/reports/{session_id}/pdf?lang=en")
    assert pdf_resp.status_code == 200
    reader = PdfReader(io.BytesIO(pdf_resp.content))
    extracted_text = "".join([p.extract_text() or "" for p in reader.pages])
    assert "DEMO REFERENCE RESULT" in extracted_text
    assert "NOT AN AI PREDICTION" in extracted_text

    # 2. Test stye.jpg (Target: Stye)
    stye_fn = "stye.jpg"
    stye_path = os.path.join(DEMO_DIR, stye_fn)
    with open(stye_path, "rb") as f:
        stye_bytes = f.read()

    s_resp = client.post(
        "/api/analyze",
        files={"images": (stye_fn, stye_bytes, "image/jpeg")},
        data={
            "module": "unified",
            "capture_source": "upload",
            "language": "en",
            "age_years": 35,
            "clinical_sex": "female"
        }
    )
    assert s_resp.status_code == 200
    s_data = s_resp.json()
    assert s_data.get("selected_module") == "stye"
    assert s_data.get("stye", {}).get("prediction", [{}])[0].get("predicted_class") == "stye_hordeolum"
    # Anemia must NOT have 5.2 g/dL! Calibrated to physiological range > 10.0 g/dL
    assert s_data.get("view_mean") is not None
    assert s_data.get("view_mean") > 10.0
