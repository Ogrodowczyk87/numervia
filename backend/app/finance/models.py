from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class MortgageInput:
    principal: Decimal
    annual_interest_rate: Decimal
    term_years: int
    monthly_overpayment: Decimal = Decimal("0.00")


@dataclass(frozen=True)
class ScheduleEntry:
    month: int
    payment: Decimal
    interest: Decimal
    principal_paid: Decimal
    extra_payment: Decimal
    remaining_balance: Decimal


@dataclass(frozen=True)
class RepaymentScenario:
    months_to_payoff: int
    total_interest: Decimal
    total_paid: Decimal
    schedule: list[ScheduleEntry]


@dataclass(frozen=True)
class MortgageComparison:
    interest_saved: Decimal
    months_saved: int


@dataclass(frozen=True)
class MortgageResult:
    monthly_payment: Decimal
    baseline: RepaymentScenario
    with_overpayment: RepaymentScenario
    comparison: MortgageComparison
    currency: str = "GBP"
