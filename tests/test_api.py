from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_calculate_endpoint_success():
    payload = {
        "gameplay_duration_seconds": 120,
        "fruits_sliced": 85,
        "fruits_missed": 10,
        "bombs_hit": 1,
        "bombs_dodged": 8,
        "max_combo": 12,
        "pause_count": 1,
        "retries": 0,
        "overall_score": 950,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "accuracy_rate" in data
    assert "response_rate" in data
    assert "error_rate" in data
    assert "persistence_rate" in data
    assert "consistency_rate" in data
    assert "overall_performance_score" in data

    # Verify ranges
    for key, val in data.items():
        assert 0.0 <= val <= 100.0, f"Rate {key} value {val} is outside [0, 100]!"


def test_calculate_endpoint_validation_error():
    # Negative fruit sliced count (invalid)
    payload = {
        "gameplay_duration_seconds": 120,
        "fruits_sliced": -5,
        "fruits_missed": 10,
        "bombs_hit": 1,
        "bombs_dodged": 8,
        "max_combo": 12,
        "pause_count": 1,
        "retries": 0,
        "overall_score": 950,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code == 422  # Unprocessable Entity
