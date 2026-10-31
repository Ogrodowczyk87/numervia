import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("principal", "0"),
        ("principal", "-1"),
        ("principal", "2000000.01"),
        ("principal", "1.001"),
        ("principal", ""),
        ("principal", "NaN"),
        ("principal", "Infinity"),
        ("principal", " 100 "),
        ("principal", 100),
        ("principal", True),
        ("principal", None),
        ("principal", []),
        ("principal", {}),
        ("annual_interest_rate", "-1"),
        ("annual_interest_rate", "20.01"),
        ("annual_interest_rate", "NaN"),
        ("annual_interest_rate", "Infinity"),
        ("annual_interest_rate", ""),
        ("annual_interest_rate", 4.5),
        ("term_years", 0),
        ("term_years", 41),
        ("term_years", 1.5),
        ("term_years", "25"),
        ("term_years", True),
        ("term_years", None),
        ("monthly_overpayment", "-1"),
        ("monthly_overpayment", "20000.01"),
        ("monthly_overpayment", "0.001"),
        ("monthly_overpayment", "NaN"),
        ("monthly_overpayment", "Infinity"),
        ("monthly_overpayment", 10),
        ("currency", "USD"),
        ("currency", None),
        ("unexpected", "value"),
    ],
)
def test_simulation_api_validation(field, value):
    payload = {
        "principal": "180000.00",
        "annual_interest_rate": "4.5",
        "term_years": 25,
    }
    payload[field] = value
    with TestClient(app) as client:
        response = client.post("/api/v1/mortgage/simulate", json=payload)
    assert response.status_code == 422
    assert any(error["loc"] == ["body", field] for error in response.json()["detail"])
