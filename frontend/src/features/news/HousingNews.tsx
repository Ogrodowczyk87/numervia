import { useEffect, useRef, useState } from "react";
import NewsCard from "./NewsCard";
import { getFinancialNews } from "./newsApi";
import type { NewsArticle } from "./newsApi";

export default function HousingNews({ excludeUrls }: { excludeUrls: string[] }) {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [visibleCount, setVisibleCount] = useState(2);
  const grid = useRef<HTMLDivElement>(null);
  const excluded = new Set(excludeUrls.map((url) => url.split("#", 1)[0]));
  const available = articles.filter((article) => !excluded.has(article.url.split("#", 1)[0]));

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const result = await getFinancialNews(controller.signal, "housing");
        if (!controller.signal.aborted) setArticles(result);
      } catch {
        if (!controller.signal.aborted) setError("Housing news is temporarily unavailable. Please try again later.");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    void load();
    return () => controller.abort();
  }, []);

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
      className="flex min-w-0 flex-col px-4 pb-16 lg:h-0 lg:min-h-[30rem] lg:flex-1"
    >
      <h2 id="housing-news-heading" className="shrink-0 text-2xl font-bold">Property & mortgages</h2>
      {(loading || error || available.length === 0) && (
        <p role="status" className="mt-4 text-sm text-muted">
          {loading ? "Loading housing news…" : error || "No housing headlines available right now."}
        </p>
      )}
      <div ref={grid} className="mt-6 grid gap-4 @min-[32rem]:grid-cols-2 lg:min-h-0 lg:flex-1 lg:auto-rows-fr">
        {available.slice(0, Math.min(visibleCount, Math.ceil(available.length / 2))).map((article) => <NewsCard key={article.url} article={article} compact />)}
      </div>
    </section>
  );
}
