import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageCalculator from "../src/features/mortgage/MortgageCalculator";
import { mortgageResult } from "./mortgageFixture";
vi.mock("../src/features/mortgage/MortgageChart", () => ({ default: () => <div>Balance chart</div> }));

test("sends one request, shows loading, then renders results and schedule", async () => {
  let resolve!: (value: Response) => void;
  const fetchMock = vi.fn(() => new Promise<Response>((done) => { resolve = done; }));
  vi.stubGlobal("fetch", fetchMock);
  render(<MortgageCalculator />);
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  expect(screen.getByRole("button", { name: "Calculating…" })).toBeDisabled();
  fireEvent.click(screen.getByRole("button", { name: "Calculating…" }));
  expect(fetchMock).toHaveBeenCalledTimes(1);
  const [url, options] = fetchMock.mock.calls[0] as unknown as [string, RequestInit];
  expect(url).toBe("/api/v1/mortgage/simulate");
  expect(options.method).toBe("POST");
  expect(JSON.parse(options.body as string)).toMatchObject({ principal: "180000.00", term_years: 25, currency: "GBP" });
  await act(async () => { resolve(new Response(JSON.stringify(mortgageResult()))); });
  expect(await screen.findByRole("heading", { name: "Results" })).toBeVisible();
  expect(screen.getByText("Balance chart")).toBeVisible();
  expect(screen.getByRole("heading", { name: "Repayment schedule" })).toBeVisible();
  expect(screen.getByRole("button", { name: "Calculate" })).toBeEnabled();
});
