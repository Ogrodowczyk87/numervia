import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test.each([503, 502])("handles API status %i", async (status) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("{}", { status })));
  render(<FinancialNews />);
  expect(await screen.findByText(status === 503 ? "Financial news is not configured yet." : /Financial news is temporarily unavailable/)).toBeInTheDocument();
});
