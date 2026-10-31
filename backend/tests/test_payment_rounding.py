from decimal import Decimal

import pytest

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    calculate_monthly_payment,
)


@pytest.mark.parametrize(
    ("principal", "expected"), [("1000.00", "83.33"), ("1000.02", "83.34")]
)
def test_payment_rounding(principal, expected):
    mortgage = MortgageInput(Decimal(principal), Decimal(0), 1)
    assert calculate_monthly_payment(mortgage) == Decimal(expected)
