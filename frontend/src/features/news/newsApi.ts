export type NewsArticle = {
  provider?: "marketaux" | "currents";
  title: string;
  url: string;
  source: string;
  published_at: string;
  image_url: string | null;
};

export async function getFinancialNews(signal: AbortSignal, feed: "overview" | "housing" = "overview"): Promise<NewsArticle[]> {
  const response = await fetch(feed === "housing" ? "/api/v1/news?feed=housing" : "/api/v1/news", {
    signal: AbortSignal.any([signal, AbortSignal.timeout(15_000)]),
  });
  if (!response.ok) {
    throw new Error(
      response.status === 429
        ? "Financial news provider request limit reached. Please try again later."
        : response.status === 503
        ? "Financial news is not configured yet."
        : "Financial news is temporarily unavailable. Please try again later.",
    );
  }
  return response.json();
}
