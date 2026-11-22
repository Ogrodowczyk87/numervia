import type { NewsArticle } from "./newsApi";
import NewsDemoPreview from "./NewsDemoPreview";
import NewsImage from "./NewsImage";

const dateFormat = new Intl.DateTimeFormat("en-GB", { dateStyle: "medium" });

function publicationDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Date unavailable" : dateFormat.format(date);
}

export default function NewsCard({ article, compact = false, demo = false }: { article: NewsArticle; compact?: boolean; demo?: boolean }) {
  return (
    <article className={`relative flex min-w-0 flex-col rounded-xl border border-line bg-surface p-5 shadow-sm sm:p-6 ${compact ? "h-full min-h-[22rem]" : "h-full"}`}>
      {demo && <NewsDemoPreview title={article.title} />}
      {!demo && <NewsImage src={article.image_url} compact={compact} />}
      <p className={`break-words text-xs font-medium text-soft ${compact ? "line-clamp-1" : ""}`}>
        {article.source} · {publicationDate(article.published_at)}
        {!demo && article.provider && ` · via ${article.provider === "currents" ? "Currents" : "Marketaux"}`}
      </p>
      {!demo && article.provider === "currents" && (
        <a href="https://currentsapi.services/" target="_blank" rel="noopener noreferrer"
          className="mt-2 text-xs text-brand hover:underline focus-visible:outline-2 focus-visible:outline-brand">
          Powered by Currents News API<span className="sr-only"> (opens in a new tab)</span>
        </a>
      )}
      <h3 className={`mt-3 break-words text-lg font-semibold leading-snug ${compact ? "line-clamp-3" : ""}`}>
        {demo ? article.title : <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:text-brand focus-visible:outline-2 focus-visible:outline-brand">
          {article.title}<span className="sr-only"> (opens in a new tab)</span>
        </a>}
      </h3>
      <p className="mt-auto pt-5 text-xs font-medium text-brand">{demo ? "Illustrative headline · Demo only" : "Read at source ↗"}</p>
    </article>
  );
}
