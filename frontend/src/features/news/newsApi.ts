import { apiUrl } from "../../config/api";
export type NewsArticle = {
  provider?: "marketaux" | "currents";
  title: string;
  url: string;
  source: string;
  published_at: string;
  image_url: string | null;
};

export type NewsFeed = {
  articles: NewsArticle[];
  feed: "overview" | "housing";
  fetched_at: string;
  fresh_until: string;
  serve_until: string;
  stale: boolean;
  demo: boolean;
};

export async function getFinancialNews(signal: AbortSignal, feed: "overview" | "housing" = "overview"): Promise<NewsFeed> {
  const response = await fetch(apiUrl(feed === "housing" ? "/api/v1/news?feed=housing" : "/api/v1/news"), {
    signal: AbortSignal.any([signal, AbortSignal.timeout(15_000)]),
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error("Financial news is temporarily unavailable. Please try again later.");
  }
  const data = await response.json();
  if (!data || data.feed !== feed || !Array.isArray(data.articles)
    || typeof data.stale !== "boolean" || typeof data.demo !== "boolean"
    || ![data.fetched_at, data.fresh_until, data.serve_until].every(
      (value) => typeof value === "string" && Number.isFinite(Date.parse(value)),
    )
    || !(Date.parse(data.fetched_at) < Date.parse(data.fresh_until)
      && Date.parse(data.fresh_until) <= Date.parse(data.serve_until))
    || Date.parse(data.serve_until) - Date.parse(data.fetched_at) > 86_400_000) {
    throw new Error("Financial news is temporarily unavailable. Please try again later.");
  }
  return data;
}
