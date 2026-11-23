import pytest
from fastapi.testclient import TestClient
from app import app

def test_health_check_payload_contract():
    client = TestClient(app)
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "modules" in data
    assert "anemia" in data["modules"]
