import re

from fastapi.testclient import TestClient

from app.main import app


def test_simulation_api_success():
    payload = {
        "principal": "1200.00",
        "annual_interest_rate": "0",
        "term_years": 1,
        "monthly_overpayment": "100.00",
        "currency": "GBP",
    }
    with TestClient(app) as client:
        response = client.post("/api/v1/mortgage/simulate", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert set(result) == {
        "currency",
        "monthly_payment",
        "baseline",
        "with_overpayment",
        "comparison",
        "assumptions",
    }
    assert result["currency"] == "GBP"
    assert result["monthly_payment"] == "100.00"
    assert result["baseline"]["months_to_payoff"] == 12
    assert result["with_overpayment"]["months_to_payoff"] == 6
    assert result["comparison"] == {"interest_saved": "0.00", "months_saved": 6}
    assert result["assumptions"]
    for scenario in [result["baseline"], result["with_overpayment"]]:
        assert scenario["total_paid"] == "1200.00"
        assert scenario["total_interest"] == "0.00"
        for row in scenario["schedule"]:
            assert isinstance(row["month"], int)
            for key in [
                "payment",
                "interest",
                "principal_paid",
                "extra_payment",
                "remaining_balance",
            ]:
                assert isinstance(row[key], str)
                assert re.fullmatch(r"\d+\.\d{2}", row[key])
        assert scenario["schedule"][-1]["remaining_balance"] == "0.00"
