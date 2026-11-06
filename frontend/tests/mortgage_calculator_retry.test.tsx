import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageCalculator from "../src/features/mortgage/MortgageCalculator";
import { mortgageResult } from "./mortgageFixture";
vi.mock("../src/features/mortgage/MortgageChart", () => ({ default: () => <div>Balance chart</div> }));

test("recovers after an error and replaces previous results", async () => {
  const first = mortgageResult(); const second = { ...first, monthly_payment: "200.00" };
  const fetchMock = vi.fn().mockRejectedValueOnce(new TypeError("Offline"))
    .mockResolvedValueOnce(new Response(JSON.stringify(first)))
    .mockResolvedValueOnce(new Response(JSON.stringify(second)));
  vi.stubGlobal("fetch", fetchMock);
  render(<MortgageCalculator />);
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  await screen.findByRole("alert");
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  await screen.findByRole("heading", { name: "Results" });
  expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  fireEvent.click(screen.getByRole("button", { name: "Calculate" }));
  await waitFor(() => expect(screen.getByText("Regular monthly payment").nextElementSibling).toHaveTextContent("£200.00"));
});
