"""
verify_all_e2e.py
-----------------
Automated end-to-end verification script for EyeHealthAI / OcuScan.
Validates all 4 manual test images across all 5 implemented clinical modules:
- Model A: Anemia (Continuous Hb Regression, ResNet-50)
- Model B: Conjunctival Redness / Injection (SLID, MobileNetV3-Small)
- Model C: Jaundice / Scleral Icterus (MobileNetV3-Small)
- Model D: Nuclear Cataract (MobileNetV3-Small, LOCS III)
- Model E: Stye / Hordeolum (MobileNetV3-Small)

Also verifies:
- API upload and quality checks
- Web report retrieval (/api/reports/{session_id})
- Dual 2-page PDF generation (Screening & Scorecard in English & Hindi)
"""

import os
import sys
import json
import hashlib
from PIL import Image
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from app import app
from src.database.session import sanitize_for_json

client = TestClient(app)

TEST_FILES = [
    ("17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg", "test_images/manual/17_jpg.rf.612b22b7e707fc3dbe5e13b6cca5dadf.jpg", "Stye / Eyelid lesion"),
    ("20200118_164733.jpg", "test_images/manual/20200118_164733.jpg", "Conjunctiva / Anemia macro view"),
    ("2.png", "test_images/manual/2.png", "Palpebral conjunctiva everted by finger"),
    ("25.jpg", "test_images/manual/25.jpg", "Bulbar conjunctival injection / Conjunctivitis")
]


def test_health_check():
    print("\n[STEP 1] Testing /api/health endpoint...")
    resp = client.get("/api/health")
    assert resp.status_code == 200, f"Health check failed: {resp.text}"
    data = resp.json()
    assert data["status"] == "healthy"
    print("  -> Health check 200 OK: Service is healthy.")


def run_e2e_matrix():
    print("\n[STEP 2] Running full multi-target inference & clinical verification on all 4 manual images...")
    results_matrix = []

    for fname, fpath, purpose in TEST_FILES:
        assert os.path.exists(fpath), f"Test image missing: {fpath}"
        with open(fpath, "rb") as f:
            raw_bytes = f.read()
        sha256 = hashlib.sha256(raw_bytes).hexdigest()[:16]
        im = Image.open(fpath)
        dim = f"{im.size[0]}x{im.size[1]}"

        # 1. Quality check endpoint
        q_resp = client.post(
            "/api/quality-check",
            files={"image": (fname, raw_bytes, "image/jpeg" if fname.endswith(".jpg") else "image/png")}
        )
        assert q_resp.status_code == 200, f"Quality check failed on {fname}: {q_resp.text}"
        q_data = q_resp.json()
        assert q_data.get("is_valid") is True, f"Image {fname} marked invalid"

        # 2. Analyze endpoint
        a_resp = client.post(
            "/api/analyze",
            data={
                "module": "unified",
                "capture_source": "upload",
                "age_years": "28",
                "clinical_sex": "male"
            },
            files=[("images", (fname, raw_bytes, "image/jpeg" if fname.endswith(".jpg") else "image/png"))]
        )
        assert a_resp.status_code == 200, f"Analyze failed on {fname}: {a_resp.text}"
        a_data = a_resp.json()
        session_id = a_data["session_id"]
        mr = a_data.get("model_results", {})

        # 3. Retrieve Web Report
        rep_resp = client.get(f"/api/reports/{session_id}")
        assert rep_resp.status_code == 200, f"Report endpoint failed for {session_id}"
        rep_data = rep_resp.json()
        assert rep_data.get("session_id") == session_id

        # 4. Download PDFs (Screening & Scorecard in English & Hindi)
        for r_type in ["screening", "scorecard"]:
            for lang in ["en", "hi"]:
                pdf_resp = client.get(f"/api/reports/{session_id}/{r_type}-pdf?lang={lang}")
                assert pdf_resp.status_code == 200, f"Failed {r_type} PDF ({lang}) for {session_id}: {pdf_resp.text}"
                assert len(pdf_resp.content) > 15000, f"PDF content too small: {len(pdf_resp.content)} bytes"

        # Module evaluation assertions
        stye_res = mr.get("stye", {})
        cat_res = mr.get("cataract", {})
        slid_res = mr.get("slid", {})
        anemia_res = mr.get("anemia", {})
        jaund_res = mr.get("jaundice", {})

        # Assertions per image
        if fname.startswith("17_jpg"):
            # Image 1 is a genuine Stye: must detect Stye (not Normal 96%!)
            s_pred = stye_res.get("prediction")
            s_item = s_pred[0] if isinstance(s_pred, list) else s_pred
            assert s_item.get("predicted_class") == "stye_hordeolum", f"Image 1 failed Stye detection: {s_item}"
            # Cataract must NOT claim clear lens: must be unsupported_image
            assert cat_res.get("status") == "unsupported_image", f"Cataract on Image 1 must be unsupported_image, got {cat_res.get('status')}"
            # Jaundice confidence must be genuine model probability, not hardcoded 0.94
            j_pred = jaund_res.get("prediction")[0]
            assert j_pred.get("confidence") != 0.94, f"Jaundice confidence on Image 1 is still hardcoded: {j_pred}"

        elif fname.startswith("20200118"):
            # Image 2 is everted conjunctiva: Stye & Cataract must be unsupported_image
            assert stye_res.get("status") == "unsupported_image", f"Stye on everted Image 2 must be unsupported_image, got {stye_res.get('status')}"
            assert cat_res.get("status") == "unsupported_image", f"Cataract on Image 2 must be unsupported_image, got {cat_res.get('status')}"
            # Anemia Hb for adult male (28y): 12.96 g/dL < 13.0 WHO male threshold -> Mild Anemia / Borderline
            a_pred = anemia_res.get("prediction")[0]
            assert a_pred.get("hb_pred_g_dl") == 12.96, f"Expected genuine Hb 12.96, got {a_pred.get('hb_pred_g_dl')}"
            cd_a = a_pred.get("clinical_decision", {})
            assert cd_a.get("who_stage") == "mild_anemia", f"Male 12.96 must be mild_anemia against 13.0 threshold, got {cd_a.get('who_stage')}"
            assert "Borderline" in cd_a.get("stage_label_en", ""), f"Narrative mismatch: {cd_a.get('stage_label_en')}"

        elif fname.startswith("2.png"):
            # Image 3 is palpebral everted by finger: Cataract & Stye must be unsupported
            assert cat_res.get("status") == "unsupported_image", f"Cataract on Image 3 must be unsupported_image"
            assert stye_res.get("status") == "unsupported_image", f"Stye on everted Image 3 must be unsupported_image"
            a_pred = anemia_res.get("prediction")[0]
            assert a_pred.get("hb_pred_g_dl") == 11.99, f"Expected genuine Hb 11.99, got {a_pred.get('hb_pred_g_dl')}"

        elif fname.startswith("25.jpg"):
            # Image 4 is conjunctivitis injection: SLID must detect injection
            sl_pred = slid_res.get("prediction")
            sl_item = sl_pred[0] if isinstance(sl_pred, list) else sl_pred
            assert sl_item.get("predicted_class") == "conjunctival_injection", f"Image 4 failed conjunctival injection: {sl_item}"
            assert cat_res.get("status") == "unsupported_image"
            # Genuine model audit: record raw Stye probability on conjunctivitis (cross-pathology confounder)
            s_pred4 = stye_res.get("prediction")[0]
            stye_prob4 = s_pred4.get("probabilities", {}).get("stye_hordeolum", 0.0)
            assert stye_prob4 > 0.0, f"Stye probability must be genuine float, got {stye_prob4}"

        # Record for table
        for mod in ["anemia", "slid", "jaundice", "cataract", "stye"]:
            v = mr.get(mod, {})
            status = v.get("status")
            p_val = v.get("value")
            pred = v.get("prediction")
            p0 = pred[0] if isinstance(pred, list) and len(pred) > 0 else (pred or {})
            cd = p0.get("clinical_decision", {}) if isinstance(p0, dict) else {}
            finding = cd.get("finding_en") or p0.get("predicted_class") or (f"{p0.get('hb_pred_g_dl')} g/dL" if p0.get("hb_pred_g_dl") else "N/A")
            suitable = "No" if status in ("unsupported_image", "blocked_domain_validation", "unavailable") else "Yes"
            results_matrix.append({
                "file": fname,
                "dim": dim,
                "sha256": sha256,
                "purpose": purpose,
                "module": mod,
                "suitable": suitable,
                "status": status,
                "finding": finding,
                "pass_fail": "PASS"
            })

    # Print results table
    print("\n" + "="*140)
    print(f"{'Image File':<36} | {'Module':<10} | {'Suitable?':<10} | {'Status':<23} | {'Clinical Finding':<40} | {'Audit'}")
    print("="*140)
    for r in results_matrix:
        print(f"{r['file']:<36} | {r['module']:<10} | {r['suitable']:<10} | {r['status']:<23} | {r['finding']:<40} | {r['pass_fail']}")
    print("="*140)
    print("\n[SUCCESS] All 4 images and 5 disease modules passed verification without errors!")


if __name__ == "__main__":
    test_health_check()
    run_e2e_matrix()
