from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.parametrize(
    ("principal", "rate", "years", "overpayment"),
    [
        ("0.01", "0", 40, "0.00"),
        ("2000000.00", "20", 40, "20000.00"),
        ("2000000.00", "0", 1, "0.00"),
        ("0.01", "20", 1, "20000.00"),
    ],
)
def test_simulation_api_boundaries(principal, rate, years, overpayment):
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/mortgage/simulate",
            json={
                "principal": principal,
                "annual_interest_rate": rate,
                "term_years": years,
                "monthly_overpayment": overpayment,
            },
        )
    assert response.status_code == 200
    data = response.json()
    for scenario_name in ("baseline", "with_overpayment"):
        scenario = data[scenario_name]
        assert scenario["schedule"][-1]["remaining_balance"] == "0.00"
        assert Decimal(scenario["total_paid"]) == Decimal(principal) + Decimal(
            scenario["total_interest"]
        )
        assert all(
            Decimal(row["remaining_balance"]) >= 0 for row in scenario["schedule"]
        )
    assert data["comparison"]["months_saved"] >= 0
    assert Decimal(data["comparison"]["interest_saved"]) >= 0
