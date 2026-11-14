import { act, render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article, newsFeed } from "./newsFixture";

test("marks saved data stale then removes expired articles without fetching again", async () => {
  vi.useFakeTimers();
  try {
    const now = Date.now();
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify(newsFeed([article], "overview", {
      fresh_until: new Date(now + 1000).toISOString(),
      serve_until: new Date(now + 2000).toISOString(),
    }))));
    vi.stubGlobal("fetch", fetchMock);
    render(<FinancialNews />);
    await act(async () => { await vi.advanceTimersByTimeAsync(0); });
    expect(screen.getByRole("article")).toBeVisible();
    await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
    expect(screen.getByText(/Showing saved news/)).toBeVisible();
    await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
    expect(screen.queryByRole("article")).not.toBeInTheDocument();
    expect(screen.getByText(/Financial news is temporarily unavailable/)).toBeVisible();
    expect(fetchMock).toHaveBeenCalledTimes(1);
  } finally {
    vi.useRealTimers();
  }
});
