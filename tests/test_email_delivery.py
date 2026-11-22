"""
tests/test_email_delivery.py
----------------------------
Comprehensive test suite for OcuScan AI automated email delivery service,
truthful delivery status reporting, SMTP integration, and retry mechanisms.
"""

import os
import smtplib
from unittest.mock import MagicMock, patch
import pytest
from starlette.testclient import TestClient

from app import app
from src.utils.email_service import (
    validate_email_address,
    build_email_body_html,
    get_smtp_configuration,
    send_report_email
)
from src.database import SessionLocal, create_session, register_user, save_model_result, update_report_email_status
from src.database.models import ReportMetadata

client = TestClient(app)


def test_validate_email_address():
    assert validate_email_address("doctor.astra@hospital.org") is True
    assert validate_email_address("patient.john@domain.co.in") is True
    assert validate_email_address("invalid-email") is False
    assert validate_email_address("") is False
    assert validate_email_address(None) is False
    assert validate_email_address("test@") is False
    assert validate_email_address("@domain.com") is False


def test_build_email_body_html():
    html_en = build_email_body_html("Jane Doe", "screening", "en", "Follow up in 6 months.")
    assert "Hello Jane Doe" in html_en
    assert "Follow up in 6 months" in html_en
    assert "RESEARCH USE ONLY" in html_en
    assert "OcuScan AI" in html_en

    html_hi = build_email_body_html("Jane Doe", "scorecard", "hi")
    assert "नमस्ते" in html_hi
    assert "तकनीकी शोध स्कोरकार्ड" in html_hi


def test_smtp_unconfigured_reporting():
    """Verify that when SMTP is unconfigured, system NEVER falsely claims success."""
    sample_pdf = b"%PDF-1.4 sample content with sufficient bytes to exceed the minimum sanity check of 100 bytes padding padding padding"
    with patch.dict(os.environ, {"SMTP_HOST": "", "SMTP_USER": "", "SMTP_PASSWORD": ""}):
        result = send_report_email(
            recipient_email="test.participant@example.com",
            pdf_bytes=sample_pdf,
            filename="Test_Report.pdf",
            report_type="screening",
            language="en",
            patient_name="Alex"
        )
        assert result["status"] == "unconfigured"
        assert result["mode"] == "unconfigured"
        assert result["sent"] is False
        assert result["can_retry"] is True
        assert "not configured" in result["message"].lower()


def test_smtp_mocked_live_delivery_success():
    """Verify that when SMTP is configured and server responds, status is 'sent'."""
    sample_pdf = b"%PDF-1.4 sample content with sufficient bytes to exceed the minimum sanity check of 100 bytes padding padding padding"
    
    mock_smtp_instance = MagicMock()
    
    with patch.dict(os.environ, {
        "SMTP_HOST": "smtp.mockserver.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "mailer@mockserver.com",
        "SMTP_PASSWORD": "MockAppPassword123",
        "SMTP_USE_TLS": "true"
    }), patch("smtplib.SMTP", return_value=mock_smtp_instance):
        mock_smtp_instance.__enter__.return_value = mock_smtp_instance
        
        result = send_report_email(
            recipient_email="verified.patient@example.com",
            pdf_bytes=sample_pdf,
            filename="Verified_Report.pdf",
            report_type="screening",
            language="en",
            patient_name="Sarah"
        )
        
        assert result["status"] == "sent"
        assert result["mode"] == "live_smtp"
        assert result["sent"] is True
        assert result["can_retry"] is False
        assert mock_smtp_instance.starttls.called
        assert mock_smtp_instance.login.called
        assert mock_smtp_instance.sendmail.called


def test_smtp_mocked_authentication_failure():
    """Verify that SMTP authentication failure reports status 'failed' with actionable message."""
    sample_pdf = b"%PDF-1.4 sample content with sufficient bytes to exceed the minimum sanity check of 100 bytes padding padding padding"
    
    mock_smtp_instance = MagicMock()
    mock_smtp_instance.login.side_effect = smtplib.SMTPAuthenticationError(535, b"Authentication credentials invalid")
    
    with patch.dict(os.environ, {
        "SMTP_HOST": "smtp.mockserver.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "mailer@mockserver.com",
        "SMTP_PASSWORD": "WrongPassword",
        "SMTP_USE_TLS": "true"
    }), patch("smtplib.SMTP", return_value=mock_smtp_instance):
        mock_smtp_instance.__enter__.return_value = mock_smtp_instance
        
        result = send_report_email(
            recipient_email="auth.fail@example.com",
            pdf_bytes=sample_pdf,
            filename="Auth_Fail_Report.pdf"
        )
        
        assert result["status"] == "failed"
        assert result["sent"] is False
        assert result["can_retry"] is True
        assert "authentication failed" in result["message"].lower()


def test_email_api_nonexistent_session():
    res = client.post(
        "/api/reports/nonexistent-session-id-99999/email",
        json={"recipient_email": "doc@hospital.com"}
    )
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


def test_email_api_invalid_email_format():
    res = client.post(
        "/api/reports/some-session/email",
        json={"recipient_email": "not-an-email"}
    )
    assert res.status_code == 422


def test_email_api_delivery_and_database_persistence():
    with SessionLocal() as db:
        user = register_user(
            db=db,
            full_name="Email Audit Patient",
            phone="+919876543210",
            email="audit.patient@hospital.org",
            age_years=38,
            clinical_sex="female",
            external_ai_consent=True,
            demographic_consent=True,
            email_delivery_consent=True
        )
        sess = create_session(
            db=db,
            user_id=user.id,
            selected_module="all_targets",
            capture_source="upload",
            view_types=["conjunctiva", "sclera", "cornea"],
            quality_summary={"all_passed": True, "laplacian_variance": 250.0, "mean_brightness": 130.0}
        )
        save_model_result(
            db=db,
            session_id=sess.id,
            module="anemia",
            prediction_value=12.5,
            unit="g/dL",
            operational_status="available_research_only",
            raw_prediction=[{"clinical_decision": "Normal hemoglobin reference range"}]
        )
        session_id = sess.id

    # Test delivery under unconfigured environment
    with patch.dict(os.environ, {"SMTP_HOST": "", "SMTP_USER": "", "SMTP_PASSWORD": ""}):
        res = client.post(
            f"/api/reports/{session_id}/email",
            json={
                "recipient_email": "audit.patient@hospital.org",
                "language": "en",
                "report_type": "screening",
                "custom_message": "Follow up recommended."
            }
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "unconfigured"
        assert data["sent"] is False
        assert data["can_retry"] is True
        assert "not configured" in data["message"].lower()

        # Verify status endpoint
        st_res = client.get(f"/api/reports/{session_id}/email-status")
        assert st_res.status_code == 200
        st_data = st_res.json()
        assert st_data["status"] == "unconfigured"
        assert st_data["recipient"] == "audit.patient@hospital.org"
        assert st_data["retry_count"] >= 1
