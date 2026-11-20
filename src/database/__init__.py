"""
src/database/__init__.py
------------------------
EyeHealthAI database package initialization.
"""

from src.database.models import (
    Base,
    UserProfile,
    ConsentRecord,
    ScreeningSession,
    ModelResult,
    ReportMetadata,
)
from src.database.session import (
    init_db,
    get_db,
    get_db_context,
    register_user,
    get_user_by_id,
    get_user_by_email,
    create_session,
    save_model_result,
    get_session_by_id,
    get_user_sessions,
    save_report_metadata,
    update_report_email_status,
    delete_user_data,
    delete_session_record,
    update_user_profile_age,
    engine,
    SessionLocal,
    sanitize_for_json,
    safe_json_dumps
)

__all__ = [
    "Base",
    "UserProfile",
    "ConsentRecord",
    "ScreeningSession",
    "ModelResult",
    "ReportMetadata",
    "init_db",
    "get_db",
    "get_db_context",
    "register_user",
    "update_user_profile_age",
    "get_user_by_id",
    "get_user_by_email",
    "create_session",
    "save_model_result",
    "get_session_by_id",
    "get_user_sessions",
    "save_report_metadata",
    "update_report_email_status",
    "delete_user_data",
    "delete_session_record",
    "engine",
    "SessionLocal",
    "sanitize_for_json",
    "safe_json_dumps"
]
