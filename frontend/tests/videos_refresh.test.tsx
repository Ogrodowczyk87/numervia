import { act, render, screen } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("marks stale and removes expired cards without polling or leaving a player mounted", async () => {
  vi.useFakeTimers();
  try {
    const now = Date.now();
    const saved = {
      ...videoFeed, updated_at: new Date(now).toISOString(),
      fresh_until: new Date(now + 1000).toISOString(),
      serve_until: new Date(now + 2000).toISOString(),
    };
    const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify(saved)));
    vi.stubGlobal("fetch", fetchMock);
    const view = render(<FinancialVideos />);
    await act(async () => { await vi.advanceTimersByTimeAsync(0); });
    expect(screen.getByRole("button", { name: "Play Finance explained" })).toBeVisible();
    await act(async () => { screen.getByRole("button", { name: "Play Finance explained" }).click(); });
    expect(screen.getByTitle("YouTube: Finance explained")).toBeVisible();
    await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
    expect(screen.getByText(/Showing previously fetched videos/)).toBeVisible();
    await act(async () => { await vi.advanceTimersByTimeAsync(1000); });
    expect(screen.queryByRole("article")).not.toBeInTheDocument();
    expect(screen.queryByTitle("YouTube: Finance explained")).not.toBeInTheDocument();
    expect(screen.getByText(/Videos are temporarily unavailable/)).toBeVisible();
    expect(fetchMock).toHaveBeenCalledTimes(1);
    view.unmount();
    await vi.advanceTimersByTimeAsync(6 * 3600 * 1000);
    expect(fetchMock).toHaveBeenCalledTimes(1);
  } finally { vi.useRealTimers(); }
});
