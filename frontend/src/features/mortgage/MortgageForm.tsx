import { useState } from "react";
import type { SubmitEvent } from "react";
import type { MortgageSimulationRequest } from "./types";

type MortgageFormProps = {
  isLoading?: boolean;
  onCalculate: (request: MortgageSimulationRequest) => void;
};

const inputClassName =
  "mt-2 w-full rounded-lg border border-line px-3 py-2 " +
  "focus:border-brand focus:outline-none focus:ring-2 focus:ring-brand/20";

export default function MortgageForm({
  onCalculate,
  isLoading = false,
}: MortgageFormProps) {
  const [principal, setPrincipal] = useState("180000.00");
  const [annualInterestRate, setAnnualInterestRate] = useState("4.5");
  const [termYears, setTermYears] = useState("25");
  const [monthlyOverpayment, setMonthlyOverpayment] = useState("200.00");

  function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
    event.preventDefault();

    onCalculate({
      principal,
      annual_interest_rate: annualInterestRate,
      term_years: Number(termYears),
      monthly_overpayment: monthlyOverpayment,
      currency: "GBP",
    });
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-5 rounded-2xl border border-line bg-surface p-6"
    >
      <h2 className="text-xl font-semibold">Mortgage calculator</h2>

      <div>
        <label htmlFor="principal" className="font-medium">
          Loan amount (£)
        </label>
        <input
          id="principal"
          name="principal"
          type="number"
          min="0.01"
          max="2000000"
          step="0.01"
          required
          value={principal}
          onChange={(event) => setPrincipal(event.target.value)}
          className={inputClassName}
        />
      </div>

      <div>
        <label htmlFor="interest-rate" className="font-medium">
          Annual interest rate (%)
        </label>
        <input
          id="interest-rate"
          name="annual_interest_rate"
          type="number"
          min="0"
          max="20"
          step="any"
          required
          value={annualInterestRate}
          onChange={(event) => setAnnualInterestRate(event.target.value)}
          className={inputClassName}
        />
      </div>

      <div>
        <label htmlFor="term-years" className="font-medium">
          Mortgage term (years)
        </label>
        <input
          id="term-years"
          name="term_years"
          type="number"
          min="1"
          max="40"
          step="1"
          required
          value={termYears}
          onChange={(event) => setTermYears(event.target.value)}
          className={inputClassName}
        />
      </div>

      <div>
        <label htmlFor="overpayment" className="font-medium">
          Monthly overpayment (£)
        </label>
        <input
          id="overpayment"
          name="monthly_overpayment"
          type="number"
          min="0"
          max="20000"
          step="0.01"
          required
          value={monthlyOverpayment}
          onChange={(event) => setMonthlyOverpayment(event.target.value)}
          className={inputClassName}
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full rounded-lg bg-brand px-4 py-3 font-semibold
                   text-canvas disabled:cursor-wait disabled:opacity-60 hover:bg-brand-hover focus-visible:outline-2
                   focus-visible:outline-offset-2 focus-visible:outline-brand"
      >
        {isLoading ? "Calculating…" : "Calculate"}
      </button>
    </form>
  );
}
