import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageSchedule from "../src/features/mortgage/MortgageSchedule";
import { mortgageResult } from "./mortgageFixture";

test("paginates twelve months and stops at each boundary", () => {
  render(<MortgageSchedule result={mortgageResult()} />);
  expect(screen.getAllByRole("row")).toHaveLength(13);
  expect(screen.getByRole("button", { name: "Previous" })).toBeDisabled();
  fireEvent.click(screen.getByRole("button", { name: "Next" }));
  expect(screen.getByRole("status")).toHaveTextContent("Page 2 of 2");
  expect(screen.getByRole("rowheader", { name: "24" })).toBeVisible();
  expect(screen.queryByRole("rowheader", { name: "1" })).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Next" })).toBeDisabled();
  fireEvent.click(screen.getByRole("button", { name: "Previous" }));
  expect(screen.getByRole("rowheader", { name: "1" })).toBeVisible();
});
