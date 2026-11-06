import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageSchedule from "../src/features/mortgage/MortgageSchedule";
import { mortgageResult } from "./mortgageFixture";

test("switching to a shorter scenario resets pagination and formats amounts", () => {
  render(<MortgageSchedule result={mortgageResult()} />);
  fireEvent.click(screen.getByRole("button", { name: "Next" }));
  fireEvent.click(screen.getByRole("button", { name: "With overpayments" }));
  expect(screen.getByRole("button", { name: "With overpayments" })).toHaveAttribute("aria-pressed", "true");
  expect(screen.getByRole("status")).toHaveTextContent("Page 1 of 1");
  expect(screen.getAllByRole("row")).toHaveLength(7);
  const firstRow = screen.getByRole("rowheader", { name: "1" }).closest("tr")!;
  expect(within(firstRow).getAllByRole("cell")[0]).toHaveTextContent("£400.00");
  expect(screen.getByRole("button", { name: "Next" })).toBeDisabled();
});
