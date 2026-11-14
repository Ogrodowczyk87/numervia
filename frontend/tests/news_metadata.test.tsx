import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article, newsFeed } from "./newsFixture";

test.each([false, true])("labels saved news and demo=%s", async (demo) => {
  const now = Date.now();
  const snapshot = newsFeed([article], "overview", {
    demo, stale: true,
    fetched_at: new Date(now - 7 * 3_600_000).toISOString(),
    fresh_until: new Date(now - 3_600_000).toISOString(),
    serve_until: new Date(now + 17 * 3_600_000).toISOString(),
  });
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(snapshot))));
  render(<FinancialNews />);
  expect(await screen.findByText(/Showing saved news/)).toBeVisible();
  expect(document.querySelector("time[datetime]" )).toHaveAttribute("datetime", snapshot.fetched_at);
  expect(!!screen.queryByText(/Synthetic headlines/)).toBe(demo);
});
