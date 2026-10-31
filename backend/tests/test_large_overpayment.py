from decimal import Decimal

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    simulate_mortgage,
)


def test_large_overpayment():
    result = simulate_mortgage(
        MortgageInput(Decimal("1000.00"), Decimal(12), 1, Decimal("20000.00"))
    )
    scenario = result.with_overpayment
    assert scenario.months_to_payoff == 1
    row = scenario.schedule[0]
    assert row.payment == Decimal("88.85")
    assert row.interest == Decimal("10.00")
    assert row.extra_payment == Decimal("921.15")
    assert row.remaining_balance == 0
    assert scenario.total_paid == Decimal("1010.00")
