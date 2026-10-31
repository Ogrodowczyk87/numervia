from decimal import ROUND_HALF_UP, Decimal

from app.finance.models import (
    MortgageComparison,
    MortgageInput,
    MortgageResult,
    RepaymentScenario,
    ScheduleEntry,
)


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


def generate_schedule(
    mortgage: MortgageInput,
    *,
    include_overpayments: bool = False,
) -> RepaymentScenario:
    monthly_payment = calculate_monthly_payment(mortgage)
    monthly_rate = mortgage.annual_interest_rate / Decimal(100) / Decimal(12)
    total_months = mortgage.term_years * 12

    balance = mortgage.principal
    total_interest = Decimal("0.00")
    total_paid = Decimal("0.00")
    schedule: list[ScheduleEntry] = []

    for month in range(1, total_months + 1):
        interest = (balance * monthly_rate).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

        amount_due = balance + interest

        if month == total_months:
            payment = amount_due
        else:
            payment = min(monthly_payment, amount_due)

        principal_paid = payment - interest
        balance = amount_due - payment

        extra_payment = Decimal("0.00")
        if include_overpayments:
            extra_payment = min(mortgage.monthly_overpayment, balance)
            balance -= extra_payment

        schedule.append(
            ScheduleEntry(
                month=month,
                payment=payment,
                interest=interest,
                principal_paid=principal_paid,
                extra_payment=extra_payment,
                remaining_balance=balance,
            )
        )

        total_interest += interest
        total_paid += payment + extra_payment

        if balance == Decimal(0):
            break

    return RepaymentScenario(
        months_to_payoff=len(schedule),
        total_interest=total_interest,
        total_paid=total_paid,
        schedule=schedule,
    )


def simulate_mortgage(mortgage: MortgageInput) -> MortgageResult:
    baseline = generate_schedule(mortgage)
    with_overpayment = generate_schedule(mortgage, include_overpayments=True)

    return MortgageResult(
        monthly_payment=calculate_monthly_payment(mortgage),
        baseline=baseline,
        with_overpayment=with_overpayment,
        comparison=MortgageComparison(
            interest_saved=baseline.total_interest - with_overpayment.total_interest,
            months_saved=baseline.months_to_payoff - with_overpayment.months_to_payoff,
        ),
    )
