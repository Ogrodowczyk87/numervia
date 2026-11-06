import type { MortgageSimulationResponse, ScheduleEntry } from "../src/features/mortgage/types";

function schedule(months: number, payment: number): ScheduleEntry[] {
  return Array.from({ length: months }, (_, index) => ({
    month: index + 1,
    payment: payment.toFixed(2),
    interest: "0.00",
    principal_paid: payment.toFixed(2),
    extra_payment: "0.00",
    remaining_balance: ((months - index - 1) * payment).toFixed(2),
  }));
}

export function mortgageResult(): MortgageSimulationResponse {
  return {
    currency: "GBP",
    monthly_payment: "100.00",
    baseline: { months_to_payoff: 24, total_interest: "0.00", total_paid: "2400.00", schedule: schedule(24, 100) },
    with_overpayment: { months_to_payoff: 6, total_interest: "0.00", total_paid: "2400.00", schedule: schedule(6, 400) },
    comparison: { interest_saved: "0.00", months_saved: 18 },
    assumptions: ["Fixed interest"],
  };
}
