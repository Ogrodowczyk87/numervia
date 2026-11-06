import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageCalculator from "../src/features/mortgage/MortgageCalculator";
import { mortgageResult } from "./mortgageFixture";
vi.mock("../src/features/mortgage/MortgageChart", () => ({ default: () => <div>Balance chart</div> }));

test.each([
  [422, "Sprawdź dane kredytu"], [500, "Backend jest niedostępny"],
  ["network", "Cannot connect"], ["timeout", "timed out"],
])("handles calculation failure %s and re-enables submission", async (kind, message) => {
  const fetchMock = vi.fn();
  if (kind === "network") fetchMock.mockRejectedValue(new TypeError("Offline"));
  else if (kind === "timeout") fetchMock.mockRejectedValue(new DOMException("Timeout", "TimeoutError"));
  else fetchMock.mockResolvedValue(new Response("{}", { status: kind as number }));
  vi.stubGlobal("fetch", fetchMock);
  render(<MortgageCalculator />);
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  expect(await screen.findByRole("alert")).toHaveTextContent(message);
  expect(screen.getByRole("button", { name: "Calculate" })).toBeEnabled();
  expect(screen.queryByRole("heading", { name: "Results" })).not.toBeInTheDocument();
});
