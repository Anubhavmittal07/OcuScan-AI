import pytest
import json
from src.inference.clinical_analytics import compute_anemia_clinical_decision
from src.database import sanitize_for_json

def test_clinical_decision_is_json_serializable():
    decision = compute_anemia_clinical_decision(hb_val=12.2, age_years=40, clinical_sex="female")
    clean = sanitize_for_json(decision)
    serialized = json.dumps(clean)
    assert len(serialized) > 0
    deserialized = json.loads(serialized)
    assert deserialized["who_stage"] == decision["who_stage"]
