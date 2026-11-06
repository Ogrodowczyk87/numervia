import { useEffect, useRef, useState } from "react";
import VideoCard from "./VideoCard";
import { getVideos } from "./videosApi";
import type { VideoFeed } from "./videosApi";

export default function FinancialVideos() {
  const [feed, setFeed] = useState<VideoFeed | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [activeId, setActiveId] = useState<string | null>(null);
  const strip = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const result = await getVideos(controller.signal);
        if (!controller.signal.aborted) { setFeed(result); setError(""); }
      } catch {
        if (!controller.signal.aborted) setError("Videos are temporarily unavailable. Please try again later.");
      } finally {
        if (!controller.signal.aborted) setLoading(false);
      }
    }
    void load();
    const interval = window.setInterval(() => { void load(); }, 6 * 60 * 60 * 1000);
    return () => { controller.abort(); window.clearInterval(interval); };
  }, []);

  function scroll(direction: number) {
    strip.current?.scrollBy({ left: direction * strip.current.clientWidth, behavior: "smooth" });
  }

  return (
    <section aria-labelledby="videos-heading" className="mx-auto max-w-5xl px-4 py-10">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 id="videos-heading" className="text-2xl font-bold">Videos</h2>
          <p className="mt-2 text-sm text-slate-600">Finance, economy and technology · From YouTube</p>
        </div>
        {!!feed?.videos.length && <div className="flex gap-2">
          <button type="button" aria-label="Previous videos" onClick={() => scroll(-1)} className="min-h-11 min-w-11 rounded-full border border-slate-300 hover:bg-slate-100">←</button>
          <button type="button" aria-label="Next videos" onClick={() => scroll(1)} className="min-h-11 min-w-11 rounded-full border border-slate-300 hover:bg-slate-100">→</button>
        </div>}
      </div>
      <p role="status" className="mt-4 text-sm text-slate-600">
        {loading ? "Loading videos…" : error || (feed?.videos.length === 0 ? "No videos available right now." : "")}
        {feed?.stale && " Showing previously fetched videos while updates are unavailable."}
      </p>
      <div ref={strip} role="region" aria-label="Video selection" tabIndex={0} className="mt-5 flex snap-x snap-mandatory gap-5 overflow-x-auto pb-4 focus-visible:outline-2 focus-visible:outline-blue-700">
        {feed?.videos.map((video) => <VideoCard key={video.video_id} video={video} active={activeId === video.video_id} onPlay={() => setActiveId(video.video_id)} />)}
      </div>
    </section>
  );
}
