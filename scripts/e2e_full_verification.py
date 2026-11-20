"""
scripts/e2e_full_verification.py
Comprehensive End-to-End Test and Verification Script for OcuScan AI.
"""

import sys
import io
import json
import base64
import requests
from PIL import Image, ImageDraw

BASE_URL = "http://127.0.0.1:8000"

def log_test(step_name: str, passed: bool, detail: str = ""):
    status = "PASS" if passed else "FAIL"
    symbol = "[OK]" if passed else "[X]"
    print(f"[{status}] {symbol} {step_name}" + (f" -> {detail}" if detail else ""))
    if not passed:
        raise AssertionError(f"Step failed: {step_name}: {detail}")

def create_synthetic_eye_image():
    """Creates a synthetic ocular image with distinct sclera, iris, and eyelid margin."""
    img = Image.new("RGB", (400, 300), color=(240, 235, 230))
    draw = ImageDraw.Draw(img)
    # Draw eye contour
    draw.ellipse((80, 70, 320, 230), fill=(255, 255, 255), outline=(120, 40, 40), width=4)
    # Draw iris
    draw.ellipse((150, 100, 250, 200), fill=(90, 60, 40), outline=(50, 30, 20), width=3)
    # Draw pupil
    draw.ellipse((180, 130, 220, 170), fill=(20, 20, 20))
    # Draw eyelid margin / conjunctiva
    draw.arc((70, 60, 330, 240), start=0, end=180, fill=(180, 50, 50), width=6)
    
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()

def main():
    print("=" * 70)
    print("OcuScan AI - Comprehensive End-to-End Production Readiness Audit")
    print("=" * 70)
    
    session = requests.Session()
    
    # 1. Health Endpoint
    res = session.get(f"{BASE_URL}/api/health")
    log_test("System Health Endpoint (/api/health)", res.status_code == 200 and res.json().get("status") == "healthy", f"HTTP {res.status_code}")
    
    # 2. System Status & Model Manifest Endpoint
    res = session.get(f"{BASE_URL}/api/status")
    log_test("System Status Endpoint (/api/status)", res.status_code == 200, f"HTTP {res.status_code}")
    status_data = res.json()
    log_test("Model Catalog Integrity", "anemia" in status_data.get("modules", {}), "Anemia regressor present")

    # 3. Model Reliability Audit Metrics
    res = session.get(f"{BASE_URL}/api/reliability-metrics")
    log_test("Reliability Metrics API (/api/reliability-metrics)", res.status_code == 200, f"HTTP {res.status_code}")
    audit_data = res.json()
    models_audit = audit_data.get("models", {})
    
    # Verify Cataract exact requested metrics (89.8, 91.3, 87.5, 93.1, 90.2)
    cataract = models_audit.get("model_d_cataract", {})
    cat_acc = cataract.get("accuracy")
    log_test("Cataract Reliability Accuracy Verification", round(cat_acc * 100, 1) == 89.8 if cat_acc < 1 else cat_acc == 89.8, f"Accuracy={cat_acc}")
    
    # Verify Stye requested metrics (98.8, 100.0, 97.8, 100.0, 98.9, Available for Evaluation)
    stye = models_audit.get("model_e_stye", {})
    stye_acc = stye.get("accuracy")
    stye_status = stye.get("lifecycle_status", "")
    log_test("Stye Reliability Accuracy Verification", round(stye_acc * 100, 1) == 98.8 if stye_acc < 1 else stye_acc == 98.8, f"Accuracy={stye_acc}")
    log_test("Stye Evaluation Status Label", "Available for Evaluation" in stye_status, f"Status: '{stye_status}'")

    # 4. User Registration with Mandatory Age & WHO Demographic Consent
    user_payload = {
        "full_name": "E2E Audit User",
        "phone": "+91 99999 88888",
        "email": "e2e.audit.user@hospital.org",
        "age_years": 42,
        "gender": "female",
        "clinical_sex": "female",
        "is_pregnant": False,
        "external_ai_consent": True,
        "demographic_consent": True,
        "research_consent": True,
        "data_storage_consent": True
    }
    res = session.post(f"{BASE_URL}/api/register", json=user_payload)
    log_test("User Registration & Informed Consent (/api/register)", res.status_code == 200, f"HTTP {res.status_code}")
    reg_data = res.json()
    user_id = reg_data.get("user", {}).get("id") or reg_data.get("id")
    log_test("User Profile Created", bool(user_id), f"User ID: {user_id}")

    # 5. Image Quality Pre-Check API
    img_bytes = create_synthetic_eye_image()
    files = {"image": ("eye_test.jpg", io.BytesIO(img_bytes), "image/jpeg")}
    res = session.post(f"{BASE_URL}/api/quality-check", files=files)
    log_test("Image Quality Verification (/api/quality-check)", res.status_code == 200, f"HTTP {res.status_code}")
    q_data = res.json()
    qual = q_data.get("quality", {})
    log_test("Quality Metric Sharpness & Brightness", "sharpness" in qual and "brightness" in qual, f"Sharpness: {qual.get('sharpness')}, Brightness: {qual.get('brightness')}")

    # 6. Eye Detection API (for real-time reticle & alignment)
    files = {"image": ("eye_detect.jpg", io.BytesIO(img_bytes), "image/jpeg")}
    res = session.post(f"{BASE_URL}/api/detect-eye", files=files)
    log_test("Eye Tracking & Macro Reticle Detection (/api/detect-eye)", res.status_code == 200, f"HTTP {res.status_code}")

    # 7. Unified Multi-View Inference Pipeline (/api/analyze)
    form_data = {
        "module": "all",
        "capture_source": "upload",
        "user_id": user_id,
        "age_years": 42,
        "clinical_sex": "female",
        "external_ai_consent": "true",
        "demographic_consent": "true"
    }
    files = [
        ("images", ("palpebral_view.jpg", io.BytesIO(img_bytes), "image/jpeg")),
        ("images", ("sclera_view.jpg", io.BytesIO(img_bytes), "image/jpeg"))
    ]
    res = session.post(f"{BASE_URL}/api/analyze", data=form_data, files=files)
    log_test("Multi-Target Inference Execution (/api/analyze)", res.status_code == 200, f"HTTP {res.status_code}")
    inference_res = res.json()
    session_id = inference_res.get("session_id")
    log_test("Screening Session Instantiated", bool(session_id), f"Session ID: {session_id}")

    # 8. Report Metadata Retrieval
    res = session.get(f"{BASE_URL}/api/reports/{session_id}")
    log_test("Session Report Data Retrieval (/api/reports/{id})", res.status_code == 200, f"HTTP {res.status_code}")

    # 9. Patient Screening PDF Generation
    res = session.get(f"{BASE_URL}/api/reports/{session_id}/screening-pdf?lang=en")
    log_test("2-Page Patient Screening PDF (English)", res.status_code == 200 and res.content.startswith(b"%PDF-1."), f"Size: {len(res.content)} bytes")

    # 10. Hindi Technical Scorecard PDF Generation
    res = session.get(f"{BASE_URL}/api/reports/{session_id}/scorecard-pdf?lang=hi")
    log_test("2-Page Technical Scorecard PDF (Hindi)", res.status_code == 200 and res.content.startswith(b"%PDF-1."), f"Size: {len(res.content)} bytes")

    # 11. Automatic Email Delivery & Audit Endpoints
    # Check automatic email dispatch result from /api/analyze
    auto_email = inference_res.get("email_delivery")
    log_test("Automatic Email Dispatch Audit", auto_email is not None, f"Auto Status: {auto_email.get('status') if auto_email else 'None'}")
    
    # Check report email status endpoint
    res = session.get(f"{BASE_URL}/api/reports/{session_id}/email-status")
    log_test("Session Email Status Audit (/api/reports/{id}/email-status)", res.status_code == 200, f"HTTP {res.status_code}")
    email_audit = res.json()
    email_status_val = email_audit.get("status") or email_audit.get("email_delivery_status")
    log_test("Email Status Truthfulness", email_status_val in ("sent", "sending", "pending", "unconfigured", "failed", "no_consent"), f"Status: {email_status_val}")

    # Check manual/retry email dispatch endpoint
    email_payload = {
        "recipient_email": "clinician.sarthak@hospital.org",
        "language": "en",
        "report_type": "screening",
        "custom_message": "Automated E2E screening verification report attached."
    }
    res = session.post(f"{BASE_URL}/api/reports/{session_id}/email", json=email_payload)
    log_test("Email Delivery API (/api/reports/{id}/email)", res.status_code == 200, f"HTTP {res.status_code}")
    email_res = res.json()
    log_test("Email Dispatch Status (Truthful Sent/Unconfigured)", email_res.get("status") in ("sent", "unconfigured", "failed"), f"Status: {email_res.get('status')}, Sent: {email_res.get('sent')}")

    # 12. Session History by User
    res = session.get(f"{BASE_URL}/api/user/{user_id}/history")
    log_test("User Session History (/api/user/{id}/history)", res.status_code == 200, f"Count: {len(res.json().get('sessions', []))}")

    # 13. Static Pages Availability
    for page in ["/", "/report", "/static/index.html", "/static/report.html"]:
        res = session.get(f"{BASE_URL}{page}")
        log_test(f"Static Route Access ({page})", res.status_code == 200, f"HTTP {res.status_code}")

    # 14. Cleanup Test Session & User
    res = session.delete(f"{BASE_URL}/api/session/{session_id}")
    log_test("Session Data Cascade Deletion", res.status_code in (200, 204), f"HTTP {res.status_code}")

    res_user = session.delete(f"{BASE_URL}/api/user/{user_id}")
    log_test("User Profile Cascade Deletion", res_user.status_code in (200, 204), f"HTTP {res_user.status_code}")

    print("=" * 70)
    print("ALL 14 END-TO-END VERIFICATION WORKFLOWS PASSED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
