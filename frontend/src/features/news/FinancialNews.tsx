import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import NewsCard from "./NewsCard";
import AdPlaceholder from "../../components/AdPlaceholder";
import HousingNews from "./HousingNews";
import { getFinancialNews } from "./newsApi";
import type { NewsArticle } from "./newsApi";

export default function FinancialNews({ sidebar }: { sidebar?: ReactNode }) {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const news = await getFinancialNews(controller.signal);
        if (!controller.signal.aborted) setArticles(news);
      } catch (cause) {
        if (!controller.signal.aborted) {
          setError(cause instanceof Error && cause.name !== "TimeoutError"
            ? cause.message
            : "Financial news is temporarily unavailable. Please try again later.");
        }
      } finally {
        if (!controller.signal.aborted) setIsLoading(false);
      }
    }
    void load();
    return () => controller.abort();
  }, []);

  const visibleArticles = articles.slice(0, Math.ceil(articles.length / 2));
  const newsSection = (
    <section aria-labelledby="news-heading" className="mx-auto max-w-5xl px-4 py-12 sm:py-16">
      <h2 id="news-heading" className="text-2xl font-bold">Financial news</h2>
      <div role="status" className="mt-4 text-sm text-muted">
        {isLoading ? "Loading financial news…" : error || (articles.length === 0 ? "No headlines available right now." : "")}
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {visibleArticles.map((article) => (
          <NewsCard key={article.url} article={article} />
        ))}
      </div>
    </section>
  );

  if (!sidebar) return newsSection;

  return (
    <div className="mx-auto grid w-full max-w-[120rem] items-start gap-6 lg:items-stretch px-4 sm:px-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)] xl:grid-cols-[16rem_minmax(0,3fr)_minmax(0,2fr)] 2xl:grid-cols-[22rem_minmax(0,3fr)_minmax(0,2fr)]">
      <AdPlaceholder />
      <div className="min-w-0">{newsSection}</div>
      <div className="@container flex min-w-0 flex-col">
        {sidebar}
        <HousingNews excludeUrls={visibleArticles.map((article) => article.url)} />
      </div>
    </div>
  );
}
