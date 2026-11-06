import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageForm from "../src/features/mortgage/MortgageForm";

test("submits edited fields using the API contract", () => {
  const onCalculate = vi.fn();
  render(<MortgageForm onCalculate={onCalculate} />);
  for (const [label, value] of [["Loan amount (£)", "250000.50"], ["Annual interest rate (%)", "3.75"], ["Mortgage term (years)", "30"], ["Monthly overpayment (£)", "500.00"]]) {
    fireEvent.change(screen.getByLabelText(label), { target: { value } });
  }
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  expect(onCalculate).toHaveBeenCalledExactlyOnceWith({ principal: "250000.50", annual_interest_rate: "3.75", term_years: 30, monthly_overpayment: "500.00", currency: "GBP" });
});
