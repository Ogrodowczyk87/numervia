import { expect, test, vi } from "vitest";
import { getFinancialNews } from "../src/features/news/newsApi";
import { article, newsFeed } from "./newsFixture";

test.each([
  [article],
  newsFeed([], "housing"),
  newsFeed([], "overview", { fetched_at: "bad-date" }),
  newsFeed([], "overview", { serve_until: new Date(Date.now() - 1).toISOString() }),
])("rejects an invalid news response", async (payload) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(payload))));
  await expect(getFinancialNews(new AbortController().signal)).rejects.toThrow(/temporarily unavailable/);
});
