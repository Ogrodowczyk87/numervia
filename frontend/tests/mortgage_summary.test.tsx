import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageSummary from "../src/features/mortgage/MortgageSummary";
import { mortgageResult } from "./mortgageFixture";

test("displays GBP values and replaces them after recalculation", () => {
  const result = mortgageResult();
  const view = render(<MortgageSummary result={result} />);
  expect(screen.getByText("Regular monthly payment").nextElementSibling).toHaveTextContent("£100.00");
  expect(screen.getByText("Time saved").nextElementSibling).toHaveTextContent("18 months");
  view.rerender(<MortgageSummary result={{ ...result, monthly_payment: "1234.56", comparison: { interest_saved: "5000.12", months_saved: 30 } }} />);
  expect(screen.getByText("Regular monthly payment").nextElementSibling).toHaveTextContent("£1,234.56");
  expect(screen.getByText("Interest saved").nextElementSibling).toHaveTextContent("£5,000.12");
  expect(screen.queryByText("18 months")).not.toBeInTheDocument();
});
