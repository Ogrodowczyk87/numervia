from decimal import Decimal

import pytest

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    generate_schedule,
)


@pytest.mark.parametrize(
    ("principal", "last_payment"), [("1000.00", "83.37"), ("1000.02", "83.28")]
)
def test_final_payment(principal, last_payment):
    result = generate_schedule(MortgageInput(Decimal(principal), Decimal(0), 1))
    assert result.months_to_payoff == 12
    assert result.schedule[-1].payment == Decimal(last_payment)
    assert result.schedule[-1].remaining_balance == 0
    assert result.total_paid == Decimal(principal)
