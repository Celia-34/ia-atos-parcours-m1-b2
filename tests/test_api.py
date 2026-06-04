"""M1-B2 — API tests.

3 tests required (health, predict valid, predict invalid).
Bonus tests welcome (deterministic, info schema, etc.).
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok(client: TestClient) -> None:
    """/health returns 200 and the expected status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_returns_ko(client: TestClient, monkeypatch) -> None:
    """/health returns 503 when model is unavailable."""
    monkeypatch.setattr(app.state, "model", None, raising=False)
    response = client.get("/health")
    assert response.status_code == 503
    assert response.json() == {"detail": "Model not loaded"}


def test_predict_valid_payload(client: TestClient, valid_payload: dict) -> None:
    """/predict returns 200 with a well-formed response on valid input.
    """
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in (0, 1)
    assert 0.0 <= data["probability"] <= 1.0
    assert "request_id" in data
    assert "model_version" in data
    pass


def test_predict_missing_field_returns_422(
    client: TestClient, valid_payload: dict
) -> None:
    """/predict returns 422 on missing required field.
    """
    invalid = {k: v for k, v in valid_payload.items() if k != "loan_amnt"}
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422
    assert "loan_amnt" in response.text
    pass


def test_info_returns_expected_5_properties(client: TestClient) -> None:
    """/info returns exactly the 5 expected metadata properties."""
    response = client.get("/info")
    assert response.status_code == 200

    data = response.json()
    expected_keys = {
        "api_version",
        "model_name",
        "model_version",
        "model_created_at",
        "metrics_holdout",
    }

    assert set(data.keys()) == expected_keys
    assert len(data) == 5


