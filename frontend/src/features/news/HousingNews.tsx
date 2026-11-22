import { useEffect, useRef, useState } from "react";
import NewsCard from "./NewsCard";
import useNewsFeed from "./useNewsFeed";
import NewsMetadata from "./NewsMetadata";

export default function HousingNews({ excludeUrls }: { excludeUrls: string[] }) {
  const { articles, snapshot, loading, error, stale } = useNewsFeed("housing");
  const [visibleCount, setVisibleCount] = useState(2);
  const grid = useRef<HTMLDivElement>(null);
  const excluded = new Set(excludeUrls.map((url) => url.split("#", 1)[0]));
  const available = articles.filter((article) => !excluded.has(article.url.split("#", 1)[0]));

  useEffect(() => {
    const element = grid.current;
    if (!element) return;
    function measure() {
      if (!window.matchMedia?.("(min-width: 1024px)").matches) {
        setVisibleCount(2);
        return;
      }
      const columns = getComputedStyle(element!).gridTemplateColumns.split(" ").length;
      // Compact cards need 352px; the gap between rows is 16px.
      const rows = Math.max(1, Math.floor((element!.clientHeight + 16) / (352 + 16)));
      setVisibleCount(rows * columns);
    }
    const observer = typeof ResizeObserver === "undefined" ? null : new ResizeObserver(measure);
    observer?.observe(element);
    window.addEventListener("resize", measure);
    measure();
    return () => {
      observer?.disconnect();
      window.removeEventListener("resize", measure);
    };
  }, [available.length]);

  return (
    <section
      aria-labelledby="housing-news-heading"
      className="flex min-w-0 flex-col px-4 pb-16 lg:h-0 lg:min-h-[35rem] lg:flex-1"
    >
      <h2 id="housing-news-heading" className="shrink-0 text-2xl font-bold">Property & mortgages</h2>
      {(loading || error || available.length === 0) && (
        <p role="status" className="mt-4 text-sm text-muted">
          {loading ? "Loading housing news…" : error || "No housing headlines available right now."}
        </p>
      )}
      {snapshot && <NewsMetadata snapshot={snapshot} stale={stale} />}
      <div ref={grid} className="mt-6 grid gap-4 @min-[32rem]:grid-cols-2 lg:min-h-0 lg:flex-1 lg:auto-rows-fr">
        {available.slice(0, Math.min(visibleCount, Math.ceil(available.length / 2))).map((article) => <NewsCard key={article.url} article={article} compact demo={snapshot?.demo} />)}
      </div>
    </section>
  );
}
