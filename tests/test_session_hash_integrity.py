import pytest
from src.inference.session_export import create_session_export, validate_session_export_schema

def test_session_export_schema_keys():
    mock_inference = {
        "status": "available_research_only",
        "prediction": []
    }
    export = create_session_export(module="anemia", inference_result=mock_inference)
    assert validate_session_export_schema(export) is True
    assert export["project"] == "EyeHealthAI"
    assert "session_id" in export
