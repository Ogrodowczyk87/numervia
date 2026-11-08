import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";

test.each([503, 502])("handles API status %i", async (status) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("{}", { status })));
  render(<FinancialNews />);
  expect(await screen.findByText(status === 503 ? "Financial news is not configured yet." : /Financial news is temporarily unavailable/)).toBeInTheDocument();
});

test("explains when the news provider request limit is reached", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("{}", { status: 429 })));
  render(<FinancialNews />);
  expect(await screen.findByText("Financial news provider request limit reached. Please try again later.")).toBeInTheDocument();
});
