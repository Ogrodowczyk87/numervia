from decimal import Decimal

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    simulate_mortgage,
)


def test_zero_overpayment():
    result = simulate_mortgage(MortgageInput(Decimal("180000.00"), Decimal("4.5"), 25))
    assert result.baseline == result.with_overpayment
    assert result.comparison.interest_saved == 0
    assert result.comparison.months_saved == 0
