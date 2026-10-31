from fastapi.testclient import TestClient

from app.main import app


def test_simulation_api_defaults():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/mortgage/simulate",
            json={"principal": "1000.00", "annual_interest_rate": "0", "term_years": 1},
        )
    assert response.status_code == 200
    result = response.json()
    assert result["currency"] == "GBP"
    assert result["baseline"] == result["with_overpayment"]
    assert result["comparison"] == {"interest_saved": "0.00", "months_saved": 0}
