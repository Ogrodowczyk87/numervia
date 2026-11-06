import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageSchedule from "../src/features/mortgage/MortgageSchedule";
import { mortgageResult } from "./mortgageFixture";

test("handles an empty schedule without navigation errors", () => {
  const result = mortgageResult(); result.baseline.schedule = [];
  render(<MortgageSchedule result={result} />);
  expect(screen.getByText("No repayment entries available.")).toBeVisible();
  expect(screen.getByRole("button", { name: "Previous" })).toBeDisabled();
  expect(screen.getByRole("button", { name: "Next" })).toBeDisabled();
});
