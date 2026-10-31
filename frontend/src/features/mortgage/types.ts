export type MortgageSimulationRequest = {
  principal: string;
  annual_interest_rate: string;
  term_years: number;
  monthly_overpayment: string;
  currency: "GBP";
};

export type ScheduleEntry = {
  month: number;
  payment: string;
  interest: string;
  principal_paid: string;
  extra_payment: string;
  remaining_balance: string;
};

export type RepaymentScenario = {
  months_to_payoff: number;
  total_interest: string;
  total_paid: string;
  schedule: ScheduleEntry[];
};

export type MortgageSimulationResponse = {
  currency: "GBP";
  monthly_payment: string;
  baseline: RepaymentScenario;
  with_overpayment: RepaymentScenario;
  comparison: {
    interest_saved: string;
    months_saved: number;
  };
  assumptions: string[];
};
