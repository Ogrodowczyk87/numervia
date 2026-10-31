import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.parametrize("field", ["principal", "annual_interest_rate", "term_years"])
def test_simulation_api_missing_fields(field):
    payload = {"principal": "1000.00", "annual_interest_rate": "0", "term_years": 1}
    del payload[field]
    with TestClient(app) as client:
        response = client.post("/api/v1/mortgage/simulate", json=payload)
    assert response.status_code == 422
    assert any(error["loc"] == ["body", field] for error in response.json()["detail"])
