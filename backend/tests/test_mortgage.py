from decimal import Decimal

from app.finance.models import MortgageInput
from app.finance.mortgage import calculate_monthly_payment


def test_mortgage_input_defaults():
    mortgage = MortgageInput(
        principal=Decimal("180000.00"),
        annual_interest_rate=Decimal("4.5"),
        term_years=25,
    )

    assert mortgage.principal == Decimal("180000.00")
    assert mortgage.annual_interest_rate == Decimal("4.5")
    assert mortgage.term_years == 25
    assert mortgage.monthly_overpayment == Decimal("0.00")


def test_monthly_payment_with_positive_interest():
    mortgage = MortgageInput(
        principal=Decimal("1000.00"),
        annual_interest_rate=Decimal(12),
        term_years=1,
    )

    payment = calculate_monthly_payment(mortgage)

    assert payment == Decimal("88.85")


def test_monthly_payment_with_zero_interest():
    mortgage = MortgageInput(
        principal=Decimal("120000.00"),
        annual_interest_rate=Decimal(0),
        term_years=25,
    )

    payment = calculate_monthly_payment(mortgage)

    assert payment == Decimal("400.00")
