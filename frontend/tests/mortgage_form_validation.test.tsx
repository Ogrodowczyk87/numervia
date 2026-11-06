import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageForm from "../src/features/mortgage/MortgageForm";

test.each([
  ["Loan amount (£)", ""], ["Loan amount (£)", "0"], ["Loan amount (£)", "2000001"], ["Loan amount (£)", "1.001"],
  ["Annual interest rate (%)", "-1"], ["Annual interest rate (%)", "21"],
  ["Mortgage term (years)", "0"], ["Mortgage term (years)", "41"], ["Mortgage term (years)", "1.5"],
  ["Monthly overpayment (£)", "-1"], ["Monthly overpayment (£)", "20001"],
])("rejects invalid %s value %s", (label, value) => {
  const onCalculate = vi.fn();
  render(<MortgageForm onCalculate={onCalculate} />);
  const input = screen.getByLabelText(label) as HTMLInputElement;
  fireEvent.change(input, { target: { value } });
  expect(input.checkValidity()).toBe(false);
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  expect(onCalculate).not.toHaveBeenCalled();
});
