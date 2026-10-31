from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, PlainSerializer, field_validator

from app.finance.models import MortgageInput

Money = Annotated[
    Decimal, PlainSerializer(lambda value: format(value, ".2f"), return_type=str)
]


class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ScheduleEntryResponse(ResponseModel):
    month: int
    payment: Money
    interest: Money
    principal_paid: Money
    extra_payment: Money
    remaining_balance: Money


class RepaymentScenarioResponse(ResponseModel):
    months_to_payoff: int
    total_interest: Money
    total_paid: Money
    schedule: list[ScheduleEntryResponse]


class MortgageComparisonResponse(ResponseModel):
    interest_saved: Money
    months_saved: int


class MortgageSimulationResponse(ResponseModel):
    currency: Literal["GBP"]
    monthly_payment: Money
    baseline: RepaymentScenarioResponse
    with_overpayment: RepaymentScenarioResponse
    comparison: MortgageComparisonResponse
    assumptions: list[str] = Field(
        default_factory=lambda: [
            "Fixed annual interest rate for the full term",
            "Monthly interest rounded to pennies using ROUND_HALF_UP",
            "Overpayments shorten the term without reducing the regular payment",
            "No early repayment charges or fees",
            "Final payment adjusted to clear the remaining balance",
        ]
    )


class MortgageSimulationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    principal: Annotated[
        Decimal, Field(gt=0, le=2_000_000, decimal_places=2, allow_inf_nan=False)
    ]
    annual_interest_rate: Annotated[Decimal, Field(ge=0, le=20, allow_inf_nan=False)]
    term_years: Annotated[int, Field(strict=True, ge=1, le=40)]
    monthly_overpayment: Annotated[
        Decimal, Field(ge=0, le=20_000, decimal_places=2, allow_inf_nan=False)
    ] = Decimal("0.00")
    currency: Literal["GBP"] = "GBP"

    @field_validator(
        "principal", "annual_interest_rate", "monthly_overpayment", mode="before"
    )
    @classmethod
    def require_decimal_string(cls, value: object) -> str:
        if not isinstance(value, str):
            # Pydantic converts ValueError into a validation error; TypeError escapes.
            raise ValueError(  # noqa: TRY004
                "Provide a decimal string, for example '180000.00'"
            )
        if not value or value != value.strip():
            raise ValueError("Provide a non-empty decimal string without whitespace")
        return value

    def to_mortgage_input(self) -> MortgageInput:
        return MortgageInput(
            principal=self.principal,
            annual_interest_rate=self.annual_interest_rate,
            term_years=self.term_years,
            monthly_overpayment=self.monthly_overpayment,
        )
