import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.mark.parametrize(
    "origin,allowed",
    [("https://demo.example.com", True), ("https://other.example.com", False)],
)
def test_cors_allows_only_configured_origin(monkeypatch, origin, allowed):
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://demo.example.com")
    with TestClient(create_app()) as client:
        preflight = client.options(
            "/api/v1/mortgage/simulate",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )
        assert preflight.status_code == (200 if allowed else 400)
        response = client.post(
            "/api/v1/mortgage/simulate", json={}, headers={"Origin": origin}
        )
        assert response.status_code == 422
        assert response.headers.get("Access-Control-Allow-Origin") == (
            origin if allowed else None
        )
