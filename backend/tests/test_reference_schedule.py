from decimal import Decimal

from app.finance.models import MortgageInput
from app.finance.mortgage import (
    generate_schedule,
)


def test_reference_schedule():
    # Independently calculated in integer pennies: monthly interest = (balance + 50) // 100.
    # £1,000 principal, 12% nominal annual rate, 12 months; regular payment £88.85.
    expected = [
        (1, "88.85", "10.00", "921.15"),
        (2, "88.85", "9.21", "841.51"),
        (3, "88.85", "8.42", "761.08"),
        (4, "88.85", "7.61", "679.84"),
        (5, "88.85", "6.80", "597.79"),
        (6, "88.85", "5.98", "514.92"),
        (7, "88.85", "5.15", "431.22"),
        (8, "88.85", "4.31", "346.68"),
        (9, "88.85", "3.47", "261.30"),
        (10, "88.85", "2.61", "175.06"),
        (11, "88.85", "1.75", "87.96"),
        (12, "88.84", "0.88", "0.00"),
    ]
    result = generate_schedule(MortgageInput(Decimal("1000.00"), Decimal(12), 1))
    actual = [
        (row.month, str(row.payment), str(row.interest), str(row.remaining_balance))
        for row in result.schedule
    ]
    assert actual == expected
    assert result.total_interest == Decimal("66.19")
