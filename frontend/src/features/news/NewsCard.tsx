import type { NewsArticle } from "./newsApi";

const dateFormat = new Intl.DateTimeFormat("en-GB", { dateStyle: "medium" });

function publicationDate(value: string) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Date unavailable" : dateFormat.format(date);
}

export default function NewsCard({ article, compact = false }: { article: NewsArticle; compact?: boolean }) {
  return (
    <article className={`relative flex min-w-0 flex-col rounded-xl border border-line bg-surface p-6 ${compact ? "h-full min-h-[22rem]" : ""}`}>
      {article.image_url && (
        <img
          src={article.image_url}
          alt=""
          width={640}
          height={360}
          loading="lazy"
          referrerPolicy="no-referrer"
          className={`mb-4 w-full rounded-lg object-cover ${compact ? "h-36" : "aspect-video"}`}
          onError={(event) => { event.currentTarget.hidden = true; }}
        />
      )}
      <p className={`break-words text-xs font-medium text-soft ${compact ? "line-clamp-1" : ""}`}>
        {article.source} · {publicationDate(article.published_at)}
        {article.provider && ` · via ${article.provider === "currents" ? "Currents" : "Marketaux"}`}
      </p>
      <h3 className={`mt-3 break-words text-lg font-semibold leading-snug ${compact ? "line-clamp-3" : ""}`}>
        <a href={article.url} target="_blank" rel="noopener noreferrer" className="hover:text-brand focus-visible:outline-2 focus-visible:outline-brand">
          {article.title}<span className="sr-only"> (opens in a new tab)</span>
        </a>
      </h3>
      <p className={`${compact ? "mt-auto pt-4" : "mt-4"} text-sm text-brand`}>Read at source ↗</p>
    </article>
  );
}
