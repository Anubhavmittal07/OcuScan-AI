"""
src/utils/email_service.py
--------------------------
OcuScan AI - Secure Clinical & Research Report Email Delivery Service.

Enforces:
1. True delivery verification: Never reports successful delivery when SMTP credentials are unconfigured or when provider rejects the email.
2. Privacy preservation: Never exposes sensitive diagnosis details or clinical risk classifications in external email subjects or preview snippets.
3. Secret security: Never leaks passwords, internal paths, or credentials in log output or error responses.
4. Flexible provider integration: Supports Gmail App Passwords, SendGrid, Amazon SES, Office 365, Mailgun, and custom institutional SMTP relays.
"""

import os
import re
import smtplib
import socket
import logging
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from typing import Optional, Dict, Any

from src.config import settings

logger = logging.getLogger("eyehealthai.email_service")

# Standard RFC 5322 regex for email validation
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_email_address(email: str) -> bool:
    """Validates standard email address syntax."""
    if not email or not isinstance(email, str):
        return False
    clean = email.strip()
    return bool(EMAIL_REGEX.match(clean)) and len(clean) <= 128


def mask_email_or_user(value: Optional[str]) -> str:
    """Safely masks username or email for secure auditing without leaking secrets."""
    if not value:
        return "None"
    val = value.strip()
    if "@" in val:
        user_part, domain = val.split("@", 1)
        masked_user = user_part[0] + "***" + (user_part[-1] if len(user_part) > 1 else "")
        return f"{masked_user}@{domain}"
    if len(val) <= 3:
        return "***"
    return val[:2] + "***" + val[-1:]


def get_smtp_configuration() -> Dict[str, Any]:
    """
    Returns current SMTP configuration status without exposing confidential secrets.
    """
    host = (os.environ["SMTP_HOST"] if "SMTP_HOST" in os.environ else (settings.SMTP_HOST or "")).strip().strip("'\"").strip()
    try:
        port = int(str(os.environ.get("SMTP_PORT", str(settings.SMTP_PORT or 587))).strip().strip("'\"").strip())
    except (ValueError, TypeError):
        port = 587
    user = (os.environ["SMTP_USER"] if "SMTP_USER" in os.environ else (settings.SMTP_USER or "")).strip().strip("'\"").strip()
    raw_pwd = os.environ.get("SMTP_PASSWORD") if "SMTP_PASSWORD" in os.environ else (settings.SMTP_PASSWORD or "")
    if raw_pwd:
        raw_pwd = str(raw_pwd).strip().strip("'\"").strip()
    pwd = raw_pwd.replace(" ", "").strip() if raw_pwd and "gmail" in (host or "").lower() else (raw_pwd.strip() if raw_pwd else "")
    from_addr = (os.environ["SMTP_FROM"] if "SMTP_FROM" in os.environ else (settings.SMTP_FROM or "")).strip().strip("'\"").strip() or (user if user else "OcuScan AI <noreply@eyehealthai.local>")
    use_ssl = settings.SMTP_USE_SSL or (os.getenv("SMTP_USE_SSL", "false").lower() in ("true", "1", "yes"))
    use_tls = settings.SMTP_USE_TLS or (os.getenv("SMTP_USE_TLS", "true").lower() in ("true", "1", "yes"))
    try:
        timeout = min(int(os.environ.get("SMTP_TIMEOUT_SECONDS", str(settings.SMTP_TIMEOUT_SECONDS or 8))), 8)
    except (ValueError, TypeError):
        timeout = 8

    is_configured = bool(host and user and pwd)

    return {
        "is_configured": is_configured,
        "host": host or None,
        "port": port,
        "user_masked": mask_email_or_user(user) if user else None,
        "from_address": from_addr,
        "use_ssl": use_ssl,
        "use_tls": use_tls,
        "timeout_seconds": timeout
    }


def build_email_body_html(
    patient_name: str,
    report_type: str,
    language: str,
    custom_message: Optional[str] = None
) -> str:
    """Constructs a responsive, accessible HTML email template."""
    is_hi = str(language).lower().startswith("hi")
    is_scorecard = str(report_type).lower() in ("scorecard", "technical", "research")

    if is_hi:
        title = "ओक्यूस्कैन एआई - नेत्र स्वास्थ्य स्क्रीनिंग रिपोर्ट" if not is_scorecard else "ओक्यूस्कैन एआई - तकनीकी शोध स्कोरकार्ड"
        greeting = f"नमस्ते {patient_name}," if patient_name and patient_name not in ("Anonymous Research Participant", "Participant") else "नमस्ते,"
        intro = "आपके हालिया गैर-इनवेसिव ओकुलर स्वास्थ्य स्क्रीनिंग की आधिकारिक पीडीएफ रिपोर्ट संलग्न है।" if not is_scorecard else "आपके सत्र का तकनीकी सत्यापन स्कोरकार्ड संलग्न है।"
        disclaimer_title = "महत्वपूर्ण चिकित्सीय अस्वीकरण (RESEARCH USE ONLY):"
        disclaimer_text = "यह रिपोर्ट कृत्रिम बुद्धिमत्ता अनुसंधान प्रोटोटाइप द्वारा केवल प्रारंभिक स्क्रीनिंग उद्देश्यों के लिए तैयार की गई है। यह किसी नेत्र रोग विशेषज्ञ (Ophthalmologist) के प्रत्यक्ष नैदानिक मूल्यांकन का विकल्प नहीं है।"
    else:
        title = "OcuScan AI - Ocular Health Screening Report" if not is_scorecard else "OcuScan AI - Technical Research Scorecard"
        greeting = f"Hello {patient_name}," if patient_name and patient_name not in ("Anonymous Research Participant", "Participant") else "Hello,"
        intro = "Please find attached the official PDF report from your non-invasive ocular health screening session." if not is_scorecard else "Please find attached the technical evaluation scorecard from your recent screening session."
        disclaimer_title = "Important Clinical Notice (RESEARCH USE ONLY):"
        disclaimer_text = "This report was generated by an artificial intelligence research prototype for investigational screening purposes only. It does NOT constitute a definitive medical diagnosis and must be interpreted by a certified clinician or ophthalmologist."

    custom_section = ""
    if custom_message and custom_message.strip():
        clean_note = custom_message.strip().replace("<", "&lt;").replace(">", "&gt;")
        custom_section = f"""
        <div style="background: #f1f5f9; border-left: 4px solid #0284c7; padding: 12px 16px; margin: 20px 0; border-radius: 4px; font-size: 13.5px; color: #1e293b;">
          <strong>Clinician / Operator Note:</strong><br>
          {clean_note}
        </div>
        """

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{title}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #334155; line-height: 1.6;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background-color: #f8fafc; padding: 24px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="background-color: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: left;">
          <!-- Header -->
          <tr>
            <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 26px 32px; color: #ffffff;">
              <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #60a5fa; margin-bottom: 4px;">
                OcuScan AI &bull; Computer Vision Screening Suite
              </div>
              <h1 style="margin: 0; font-size: 20px; font-weight: 700; color: #ffffff;">
                {title}
              </h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 30px 32px;">
              <p style="font-size: 15px; font-weight: 600; color: #0f172a; margin-top: 0;">
                {greeting}
              </p>
              <p style="font-size: 13.5px; color: #475569;">
                {intro}
              </p>

              {custom_section}

              <div style="background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 18px; margin: 22px 0; text-align: center;">
                <span style="font-size: 24px;">📎</span>
                <p style="margin: 8px 0 0 0; font-size: 13px; font-weight: 700; color: #0f172a;">
                  PDF Screening Report Attached
                </p>
                <p style="margin: 4px 0 0 0; font-size: 12px; color: #64748b;">
                  Open the attachment to view complete biometric, hemoglobin, conjunctival, and icterus analysis.
                </p>
              </div>

              <!-- Disclaimer Box -->
              <div style="background-color: #fffbeb; border: 1px solid #fef3c7; border-radius: 8px; padding: 14px 16px; margin-top: 20px;">
                <p style="margin: 0 0 6px 0; font-size: 12px; font-weight: 700; color: #b45309;">
                  ⚠️ {disclaimer_title}
                </p>
                <p style="margin: 0; font-size: 11.5px; color: #78350f; line-height: 1.5;">
                  {disclaimer_text}
                </p>
              </div>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f1f5f9; padding: 18px 32px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #64748b; text-align: center;">
              OcuScan AI &bull; Multi-Target Ocular Computer Vision Framework &bull; Research Use Only<br>
              Generated securely on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""
    return html


def _connect_smtp_resilient(
    host: str,
    port: int,
    timeout: float = 8.0,
    use_ssl: bool = False
) -> smtplib.SMTP:
    """
    Establishes an SMTP connection with DNS sanitation, IPv4 resolution fallback,
    and Anycast IP fallback for standard providers like Gmail.
    Uses local_hostname='127.0.0.1' to prevent Windows reverse DNS resolution failures (Errno 11001).
    """
    clean_host = str(host).strip().strip("'\"").strip()
    import time

    last_err = None
    # Retry loop with short backoff for transient DNS / socket hiccups
    for attempt in range(3):
        try:
            if use_ssl:
                return smtplib.SMTP_SSL(clean_host, port, timeout=timeout, local_hostname="127.0.0.1")
            else:
                return smtplib.SMTP(clean_host, port, timeout=timeout, local_hostname="127.0.0.1")
        except (socket.gaierror, socket.timeout, ConnectionRefusedError, OSError) as conn_err:
            last_err = conn_err
            logger.warning(f"SMTP attempt {attempt + 1}/3 to '{clean_host}:{port}' failed ({conn_err}).")
            if attempt < 2:
                time.sleep(1.0)

    # Initiating resilient IPv4 / DNS fallback
    logger.warning(f"Standard SMTP connection to '{clean_host}:{port}' failed after 3 attempts ({last_err}). Initiating resilient IPv4 / DNS fallback...")

    # 2. Try explicit IPv4 resolution to bypass Windows IPv6 stalls / Errno 11001
    resolved_ip = None
    try:
        addr_infos = socket.getaddrinfo(clean_host, port, socket.AF_INET, socket.SOCK_STREAM)
        if addr_infos:
            resolved_ip = addr_infos[0][4][0]
    except Exception as dns_err:
        logger.warning(f"Direct IPv4 getaddrinfo failed for {clean_host}: {dns_err}")

    # 3. Provider-specific Anycast IPv4 fallbacks if DNS is completely blocked
    if not resolved_ip and "gmail" in clean_host.lower():
        for fallback_ip in ["142.250.141.108", "173.194.202.108", "74.125.133.108", "192.178.158.108"]:
            try:
                test_sock = socket.create_connection((fallback_ip, port), timeout=3.0)
                test_sock.close()
                resolved_ip = fallback_ip
                logger.info(f"Verified Google Anycast SMTP IP reachable: {resolved_ip}")
                break
            except Exception:
                continue

    if resolved_ip:
        logger.info(f"Connecting to SMTP relay using verified IPv4 endpoint {resolved_ip}:{port} for {clean_host}...")
        if use_ssl:
            server = smtplib.SMTP_SSL(resolved_ip, port, timeout=timeout, local_hostname="127.0.0.1")
        else:
            server = smtplib.SMTP(resolved_ip, port, timeout=timeout, local_hostname="127.0.0.1")
        server._host = clean_host
        return server

    if last_err:
        raise last_err
    raise socket.gaierror(11001, f"Failed to connect to SMTP host {clean_host}")


def send_report_email(
    recipient_email: str,
    pdf_bytes: bytes,
    filename: str,
    report_type: str = "screening",
    language: str = "en",
    patient_name: str = "Participant",
    custom_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Delivers a screening report or scorecard PDF to the specified recipient via SMTP.
    
    TRUTHFUL REPORTING:
    - If SMTP credentials are configured: Attempts real SMTP delivery. Returns status 'sent' on success, or 'failed' on rejection/network error.
    - If SMTP credentials are NOT configured: Explicitly returns status 'unconfigured' and sent=False. NEVER claims successful delivery when no mail was sent!
    """
    clean_email = recipient_email.strip()
    if not validate_email_address(clean_email):
        raise ValueError(f"Invalid recipient email address format: '{clean_email}'")

    if not pdf_bytes or len(pdf_bytes) < 100:
        raise ValueError("Cannot dispatch an empty or corrupted PDF document.")

    is_hi = str(language).lower().startswith("hi")
    is_scorecard = str(report_type).lower() in ("scorecard", "technical", "research")

    # Secure generic subject line: Never expose specific clinical diagnoses or risk tiers on lockscreens
    if is_hi:
        subject = f"ओक्यूस्कैन एआई - {'तकनीकी शोध स्कोरकार्ड' if is_scorecard else 'नेत्र स्क्रीनिंग रिपोर्ट'}"
    else:
        subject = f"OcuScan AI - {'Technical Research Scorecard' if is_scorecard else 'Ocular Screening Report'}"

    # Build MIME structure
    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["To"] = clean_email

    cfg = get_smtp_configuration()
    smtp_host = cfg["host"]
    smtp_port = cfg["port"]
    smtp_user = (os.environ["SMTP_USER"] if "SMTP_USER" in os.environ else (settings.SMTP_USER or "")).strip()
    raw_pass = os.environ.get("SMTP_PASSWORD") if "SMTP_PASSWORD" in os.environ else (settings.SMTP_PASSWORD or "")
    smtp_pass = raw_pass.replace(" ", "").strip() if raw_pass and "gmail" in (smtp_host or "").lower() else (raw_pass.strip() if raw_pass else "")
    smtp_from = cfg["from_address"]
    use_ssl = cfg["use_ssl"]
    use_tls = cfg["use_tls"]
    timeout = cfg["timeout_seconds"]

    msg["From"] = smtp_from

    # Body alternative (plain + HTML)
    body_part = MIMEMultipart("alternative")
    plain_text = (
        f"OcuScan AI Screening Report is attached for {clean_email}.\n"
        f"Document: {filename}\n"
        f"Generated: {datetime.now(timezone.utc).isoformat()}\n"
        "RESEARCH USE ONLY: Prototype service. Not certified for clinical diagnostic use."
    )
    body_part.attach(MIMEText(plain_text, "plain", "utf-8"))

    html_content = build_email_body_html(
        patient_name=patient_name,
        report_type=report_type,
        language=language,
        custom_message=custom_message
    )
    body_part.attach(MIMEText(html_content, "html", "utf-8"))
    msg.attach(body_part)

    # Attach PDF
    pdf_attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
    pdf_attachment.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(pdf_attachment)

    # Check configuration truth
    if not cfg["is_configured"]:
        logger.info(
            f"Email delivery skipped for '{clean_email}': SMTP_HOST, SMTP_USER, or SMTP_PASSWORD not configured. "
            f"Preserving PDF ({len(pdf_bytes)} bytes) for manual download."
        )
        return {
            "status": "unconfigured",
            "mode": "unconfigured",
            "sent": False,
            "recipient": clean_email,
            "message": "SMTP credentials are not configured on this server. The PDF report has been securely generated and preserved for direct download.",
            "filename": filename,
            "attachment_size_bytes": len(pdf_bytes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "can_retry": True
        }

    # Attempt Real SMTP Delivery
    try:
        logger.info(f"Connecting to SMTP relay {smtp_host}:{smtp_port} for recipient {clean_email}...")
        server = _connect_smtp_resilient(smtp_host, smtp_port, timeout=timeout, use_ssl=use_ssl)
        with server:
            if not use_ssl and use_tls:
                server.starttls()
            server.login(smtp_user, smtp_pass)
            import email.utils
            _, clean_envelope_from = email.utils.parseaddr(smtp_from)
            envelope_sender = clean_envelope_from or smtp_user
            server.sendmail(envelope_sender, [clean_email], msg.as_string())

        logger.info(f"Successfully transmitted email to {clean_email} via SMTP relay {smtp_host}")
        return {
            "status": "sent",
            "mode": "live_smtp",
            "sent": True,
            "recipient": clean_email,
            "message": f"Screening report PDF was successfully delivered to {clean_email} via SMTP relay.",
            "filename": filename,
            "attachment_size_bytes": len(pdf_bytes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "can_retry": False
        }
    except smtplib.SMTPAuthenticationError as auth_err:
        err_msg = "SMTP authentication failed. Verify SMTP_USER and SMTP_PASSWORD / App Password."
        logger.error(f"SMTP authentication failure: {auth_err}")
        return {
            "status": "failed",
            "mode": "live_smtp",
            "sent": False,
            "recipient": clean_email,
            "error": err_msg,
            "message": err_msg,
            "filename": filename,
            "attachment_size_bytes": len(pdf_bytes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "can_retry": True
        }
    except (smtplib.SMTPConnectError, socket.gaierror, socket.timeout, ConnectionRefusedError, OSError) as conn_err:
        err_msg = f"Unable to reach SMTP server ({smtp_host}:{smtp_port}): {conn_err}. Report is preserved for download."
        logger.error(f"SMTP connection failure: {conn_err}")
        return {
            "status": "failed",
            "mode": "live_smtp",
            "sent": False,
            "recipient": clean_email,
            "error": err_msg,
            "message": err_msg,
            "filename": filename,
            "attachment_size_bytes": len(pdf_bytes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "can_retry": True
        }
    except Exception as exc:
        err_msg = f"SMTP transmission error: {str(exc)}"
        logger.error(f"SMTP transmission exception for {clean_email}: {exc}", exc_info=True)
        return {
            "status": "failed",
            "mode": "live_smtp",
            "sent": False,
            "recipient": clean_email,
            "error": err_msg,
            "message": err_msg,
            "filename": filename,
            "attachment_size_bytes": len(pdf_bytes),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "can_retry": True
        }
