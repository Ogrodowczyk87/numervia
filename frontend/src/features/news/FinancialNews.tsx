import { useEffect, useState } from "react";
import { getFinancialNews } from "./newsApi";
import type { NewsArticle } from "./newsApi";

const dateFormat = new Intl.DateTimeFormat("en-GB", { dateStyle: "medium" });

function publicationDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Date unavailable" : dateFormat.format(date);
}

export default function FinancialNews() {
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

  return (
    <section aria-labelledby="news-heading" className="mx-auto max-w-5xl px-4 py-12 sm:py-16">
      <h2 id="news-heading" className="text-2xl font-bold">Financial news</h2>
      <div role="status" className="mt-4 text-sm text-muted">
        {isLoading ? "Loading financial news…" : error || (articles.length === 0 ? "No headlines available right now." : "")}
      </div>
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {articles.map((article) => (
          <article key={article.url} className="flex min-w-0 flex-col rounded-xl border border-line bg-surface p-6">
            {article.image_url && (
              <img
                src={article.image_url}
                alt=""
                width={640}
                height={360}
                loading="lazy"
                referrerPolicy="no-referrer"
                className="mb-4 aspect-video w-full rounded-lg object-cover"
                onError={(event) => { event.currentTarget.hidden = true; }}
              />
            )}
            <p className="break-words text-xs font-medium text-soft">
              {article.source} · {publicationDate(article.published_at)}
            </p>
            <h3 className="mt-3 break-words text-lg font-semibold leading-snug">
              <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:text-brand focus-visible:outline-2 focus-visible:outline-brand">
                {article.title}<span className="sr-only"> (opens in a new tab)</span>
              </a>
            </h3>
            <p className="mt-4 text-sm text-brand">Read at source ↗</p>
          </article>
        ))}
      </div>
    </section>
  );
}
