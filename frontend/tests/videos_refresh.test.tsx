import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("refreshes after six hours and stops polling on unmount", async () => {
  vi.useFakeTimers();
  try {
    const fetchMock = vi.fn().mockImplementation(async () => new Response(JSON.stringify(videoFeed)));
    vi.stubGlobal("fetch", fetchMock);
    const view = render(<FinancialVideos />);
    await act(async () => { await vi.advanceTimersByTimeAsync(0); });
    expect(fetchMock).toHaveBeenCalledTimes(1);
    await act(async () => { await vi.advanceTimersByTimeAsync(6 * 3600 * 1000); });
    expect(fetchMock).toHaveBeenCalledTimes(2);
    view.unmount();
    await vi.advanceTimersByTimeAsync(6 * 3600 * 1000);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  } finally { vi.useRealTimers(); }
});
