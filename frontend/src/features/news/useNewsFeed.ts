import { useEffect, useState } from "react";
import { getFinancialNews } from "./newsApi";
import type { NewsFeed } from "./newsApi";

export default function useNewsFeed(feed: "overview" | "housing") {
  const [snapshot, setSnapshot] = useState<NewsFeed | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [now, setNow] = useState(Date.now);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError("");
    setSnapshot(null);
    async function load() {
      try {
        const result = await getFinancialNews(controller.signal, feed);
        if (!controller.signal.aborted) {
          setSnapshot(result);
          setNow(Date.now());
        }
      } catch {
        if (!controller.signal.aborted) {
          setError(feed === "housing"
            ? "Housing news is temporarily unavailable. Please try again later."
            : "Financial news is temporarily unavailable. Please try again later.");
        }
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    void load();
    return () => controller.abort();
  }, [feed]);

  useEffect(() => {
    if (!snapshot) return;
    const deadlines = [snapshot.fresh_until, snapshot.serve_until].map(Date.parse);
    const next = deadlines.filter((deadline) => deadline > now).sort((a, b) => a - b)[0];
    const timer = next === undefined ? undefined : window.setTimeout(
      () => setNow(Date.now()), Math.min(2_147_483_647, Math.max(1, next - Date.now())),
    );
    const update = () => setNow(Date.now());
    document.addEventListener("visibilitychange", update);
    return () => {
      window.clearTimeout(timer);
      document.removeEventListener("visibilitychange", update);
    };
  }, [snapshot, now]);

  const expired = !!snapshot && now >= Date.parse(snapshot.serve_until);
  const usable = expired ? null : snapshot;
  return {
    snapshot: usable,
    articles: usable?.articles ?? [],
    loading,
    error: expired ? (feed === "housing"
      ? "Housing news is temporarily unavailable. Please try again later."
      : "Financial news is temporarily unavailable. Please try again later.") : error,
    stale: !!usable && (usable.stale || now >= Date.parse(usable.fresh_until)),
  };
}
