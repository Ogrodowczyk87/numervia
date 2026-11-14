import { afterEach, expect, test, vi } from "vitest";
import { simulateMortgage } from "../src/features/mortgage/mortgageApi";
import { getFinancialNews } from "../src/features/news/newsApi";
import { getVideos } from "../src/features/videos/videosApi";
import { mortgageResult } from "./mortgageFixture";
import { newsFeed } from "./newsFixture";
import { videoFeed } from "./videoFixture";

afterEach(() => vi.unstubAllEnvs());

test("all three clients use the configured backend origin", async () => {
  vi.stubEnv("VITE_API_BASE_URL", "https://api.example.com");
  const fetchMock = vi.fn()
    .mockResolvedValueOnce(new Response(JSON.stringify(mortgageResult())))
    .mockResolvedValueOnce(new Response(JSON.stringify(newsFeed([], "housing"))))
    .mockResolvedValueOnce(new Response(JSON.stringify(videoFeed)));
  vi.stubGlobal("fetch", fetchMock);
  await simulateMortgage({ principal: "180000", annual_interest_rate: "4.5", term_years: 25, monthly_overpayment: "200", currency: "GBP" });
  await getFinancialNews(new AbortController().signal, "housing");
  await getVideos(new AbortController().signal);
  expect(fetchMock.mock.calls.map(([url]) => url)).toEqual([
    "https://api.example.com/api/v1/mortgage/simulate",
    "https://api.example.com/api/v1/news?feed=housing",
    "https://api.example.com/api/v1/videos",
  ]);
});
