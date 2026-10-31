from decimal import Decimal

import pytest

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    simulate_mortgage,
)


@pytest.mark.parametrize("rate", ["0", "0.01", "4.5", "20"])
def test_positive_overpayment(rate):
    result = simulate_mortgage(
        MortgageInput(Decimal("180000.00"), Decimal(rate), 25, Decimal("200.00"))
    )
    assert result.with_overpayment.months_to_payoff < result.baseline.months_to_payoff
    assert result.with_overpayment.total_interest <= result.baseline.total_interest
    assert (
        result.comparison.months_saved
        == result.baseline.months_to_payoff - result.with_overpayment.months_to_payoff
    )
    assert (
        result.comparison.interest_saved
        == result.baseline.total_interest - result.with_overpayment.total_interest
    )
    assert (
        result.with_overpayment.schedule[0].payment
        == result.baseline.schedule[0].payment
        == result.monthly_payment
    )
