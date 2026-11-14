import { useEffect, useRef, useState } from "react";
import VideoCard from "./VideoCard";
import { getVideos } from "./videosApi";
import type { VideoFeed } from "./videosApi";

export default function FinancialVideos() {
  const [feed, setFeed] = useState<VideoFeed | null>(null);
  const [now, setNow] = useState(Date.now);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [activeId, setActiveId] = useState<string | null>(null);
  const strip = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const result = await getVideos(controller.signal);
        if (!controller.signal.aborted) { setFeed(result); setNow(Date.now()); setError(""); }
      } catch {
        if (!controller.signal.aborted) setError("Videos are temporarily unavailable. Please try again later.");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    void load();
    return () => controller.abort();
  }, []);

  useEffect(() => {
    if (!feed) return;
    const next = [feed.fresh_until, feed.serve_until].map(Date.parse)
      .filter((deadline) => deadline > now).sort((a, b) => a - b)[0];
    const timer = next === undefined ? undefined : window.setTimeout(
      () => setNow(Date.now()), Math.min(2_147_483_647, Math.max(1, next - Date.now())),
    );
    const update = () => setNow(Date.now());
    document.addEventListener("visibilitychange", update);
    return () => {
      window.clearTimeout(timer);
      document.removeEventListener("visibilitychange", update);
    };
  }, [feed, now]);

  const expired = !!feed && now >= Date.parse(feed.serve_until);
  const visibleFeed = expired ? null : feed;
  const stale = !!visibleFeed && (visibleFeed.stale || now >= Date.parse(visibleFeed.fresh_until));

  function scroll(direction: number) {
    strip.current?.scrollBy({ left: direction * strip.current.clientWidth, behavior: "smooth" });
  }

  return (
    <section aria-labelledby="videos-heading" className="mx-auto max-w-5xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 id="videos-heading" className="text-2xl font-bold">Videos</h2>
          <p className="mt-2 text-sm text-muted">Finance, economy and technology · {visibleFeed?.demo ? "Demo previews" : "From YouTube"}</p>
        </div>
        {!!visibleFeed?.videos.length && <div className="flex gap-2">
          <button type="button" aria-label="Previous videos" onClick={() => scroll(-1)} className="min-h-11 min-w-11 rounded-full border border-line hover:bg-surface-raised">←</button>
          <button type="button" aria-label="Next videos" onClick={() => scroll(1)} className="min-h-11 min-w-11 rounded-full border border-line hover:bg-surface-raised">→</button>
        </div>}
      </div>
      <p role="status" className="mt-4 text-sm text-muted">
        {loading ? "Loading videos…" : (expired ? "Videos are temporarily unavailable. Please try again later." : error) || (visibleFeed?.videos.length === 0 ? "No videos available right now." : "")}
        {stale && " Showing previously fetched videos while updates are unavailable."}
      </p>
      {visibleFeed && <p className="mt-3 text-sm text-muted">
        {visibleFeed.demo && <span className="mr-2 font-semibold text-brand">Demo videos · Synthetic previews.</span>}{" "}
        Last updated <time dateTime={visibleFeed.updated_at}>{new Date(visibleFeed.updated_at).toLocaleString()}</time>.
      </p>}
      <div ref={strip} role="region" aria-label="Video selection" tabIndex={0} className="mt-5 flex snap-x snap-mandatory gap-5 overflow-x-auto pb-4 focus-visible:outline-2 focus-visible:outline-brand">
        {visibleFeed?.videos.map((video) => <VideoCard key={video.video_id} video={video} active={activeId === video.video_id} onPlay={() => setActiveId(video.video_id)} demo={visibleFeed.demo} />)}
      </div>
    </section>
  );
}
