import pytest
from datetime import datetime
from src.inference.session_export import create_session_export

def test_session_timestamp_is_iso8601_utc():
    export = create_session_export(module="anemia", inference_result={"status": "available_research_only"})
    ts = export["timestamp_utc"]
    parsed = datetime.fromisoformat(ts)
    assert parsed.tzinfo is not None
