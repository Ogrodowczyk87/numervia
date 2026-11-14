export const article = {
  title: "Markets update",
  url: "https://example.com/news",
  source: "example.com",
  published_at: "2026-11-06T12:00:00Z",
  image_url: "https://example.com/image.jpg",
};

import type { NewsArticle, NewsFeed } from "../src/features/news/newsApi";

export function newsFeed(
  articles: NewsArticle[] = [],
  feed: "overview" | "housing" = "overview",
  overrides: Partial<NewsFeed> = {},
): NewsFeed {
  const now = Date.now();
  return {
    articles, feed,
    fetched_at: new Date(now).toISOString(),
    fresh_until: new Date(now + 6 * 3_600_000).toISOString(),
    serve_until: new Date(now + 24 * 3_600_000).toISOString(),
    stale: false, demo: false, ...overrides,
  };
}
