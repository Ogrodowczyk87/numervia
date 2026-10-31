from decimal import Decimal

import pytest

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    generate_schedule,
)


@pytest.mark.parametrize("rate", ["0", "0.01", "4.5", "20"])
@pytest.mark.parametrize("extra", ["0.00", "200.00"])
def test_schedule_accounting(rate, extra):
    mortgage = MortgageInput(Decimal("180000.00"), Decimal(rate), 40, Decimal(extra))
    result = generate_schedule(mortgage, include_overpayments=True)
    assert result.months_to_payoff == len(result.schedule)
    assert result.schedule[-1].remaining_balance == Decimal(0)
    previous_balance = mortgage.principal
    for month, row in enumerate(result.schedule, start=1):
        assert row.month == month
        assert row.remaining_balance >= 0
        assert row.payment == row.interest + row.principal_paid
        assert (
            previous_balance - row.principal_paid - row.extra_payment
            == row.remaining_balance
        )
        previous_balance = row.remaining_balance
    assert sum(row.interest for row in result.schedule) == result.total_interest
    assert (
        sum(row.payment + row.extra_payment for row in result.schedule)
        == result.total_paid
    )
    assert (
        sum(row.principal_paid + row.extra_payment for row in result.schedule)
        == mortgage.principal
    )
    assert result.total_paid == mortgage.principal + result.total_interest
    if Decimal(rate) == 0:
        assert result.total_interest == 0
