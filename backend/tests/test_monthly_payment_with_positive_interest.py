from decimal import Decimal

from app.finance.models import MortgageInput
from app.finance.mortgage import calculate_monthly_payment


def test_monthly_payment_with_positive_interest():
    mortgage = MortgageInput(
        principal=Decimal("1000.00"),
        annual_interest_rate=Decimal(12),
        term_years=1,
    )

    payment = calculate_monthly_payment(mortgage)

    assert payment == Decimal("88.85")
