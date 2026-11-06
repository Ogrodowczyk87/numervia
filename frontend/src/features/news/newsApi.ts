export type NewsArticle = {
  title: string;
  url: string;
  source: string;
  published_at: string;
  image_url: string | null;
};

export async function getFinancialNews(signal: AbortSignal): Promise<NewsArticle[]> {
  const response = await fetch("/api/v1/news", {
    signal: AbortSignal.any([signal, AbortSignal.timeout(15_000)]),
  });
  if (!response.ok) {
    throw new Error(
      response.status === 503
        ? "Financial news is not configured yet."
        : "Financial news is temporarily unavailable. Please try again later.",
    );
  }
  return response.json();
}
