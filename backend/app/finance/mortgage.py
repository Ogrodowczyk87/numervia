from decimal import ROUND_HALF_UP, Decimal

from app.finance.models import MortgageInput


def calculate_monthly_payment(mortgage: MortgageInput) -> Decimal:
    months = mortgage.term_years * 12

    if mortgage.annual_interest_rate == Decimal(0):
        payment = mortgage.principal / months
        return payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    monthly_rate = mortgage.annual_interest_rate / Decimal(100) / Decimal(12)

    payment = (
        mortgage.principal
        * monthly_rate
        / (Decimal(1) - (Decimal(1) + monthly_rate) ** (-months))
    )

    return payment.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
