import pytest
from src.inference.session_export import create_session_export, validate_session_export_schema

def test_session_export_with_empty_inputs():
    export = create_session_export(
        module="anemia", inference_result={"status": "available_research_only"}, filenames=[]
    )
    assert validate_session_export_schema(export) is True
    assert export["input_files"] == []

def test_session_export_with_none_inputs():
    export = create_session_export(
        module="anemia", inference_result={"status": "available_research_only"}, filenames=None
    )
    assert validate_session_export_schema(export) is True
    assert export["input_files"] == []
