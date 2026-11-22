import type { ReactNode } from "react";
import NewsCard from "./NewsCard";
import AdPlaceholder from "../../components/AdPlaceholder";
import HousingNews from "./HousingNews";
import useNewsFeed from "./useNewsFeed";
import NewsMetadata from "./NewsMetadata";

export default function FinancialNews({ sidebar }: { sidebar?: ReactNode }) {
  const { articles, snapshot, loading: isLoading, error, stale } = useNewsFeed("overview");

  const visibleArticles = articles.slice(0, snapshot?.demo || snapshot?.preview ? 6 : Math.ceil(articles.length / 2));
  const newsSection = (
    <section aria-labelledby="news-heading" className="mx-auto max-w-5xl px-4 py-12 sm:py-16 lg:flex lg:h-full lg:w-full lg:flex-col">
      <h2 id="news-heading" className="text-2xl font-bold">Financial news</h2>
      <div role="status" className="mt-4 text-sm text-muted">
        {isLoading ? "Loading financial news…" : error || (articles.length === 0 ? "No headlines available right now." : "")}
      </div>
      {snapshot && <NewsMetadata snapshot={snapshot} stale={stale} />}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:flex-1 lg:auto-rows-fr">
        {visibleArticles.map((article) => (
          <NewsCard key={article.url} article={article} demo={snapshot?.demo} />
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
