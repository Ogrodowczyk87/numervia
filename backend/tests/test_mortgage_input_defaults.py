from decimal import Decimal

from app.finance.models import MortgageInput


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
