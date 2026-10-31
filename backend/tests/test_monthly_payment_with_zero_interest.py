from decimal import Decimal

from app.finance.models import MortgageInput
from app.finance.mortgage import calculate_monthly_payment


def test_monthly_payment_with_zero_interest():
    mortgage = MortgageInput(
        principal=Decimal("120000.00"),
        annual_interest_rate=Decimal(0),
        term_years=25,
    )

    payment = calculate_monthly_payment(mortgage)

    assert payment == Decimal("400.00")
