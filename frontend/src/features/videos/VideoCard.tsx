import { useState } from "react";
import type { Video } from "./videosApi";

export default function VideoCard({ video, active, onPlay }: {
  video: Video; active: boolean; onPlay: () => void;
}) {
  const [imageFailed, setImageFailed] = useState(false);
  return (
    <article className="relative w-72 shrink-0 snap-start overflow-hidden rounded-2xl border border-line bg-surface sm:w-80">
      {active ? (
        <iframe
          title={`YouTube: ${video.title}`}
          src={`https://www.youtube-nocookie.com/embed/${video.video_id}?autoplay=1`}
          allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
          allowFullScreen
          referrerPolicy="strict-origin-when-cross-origin"
          className="h-56 w-full"
        />
      ) : (
        <button type="button" onClick={onPlay} aria-label={`Play ${video.title}`} className="relative block h-56 w-full bg-canvas focus-visible:outline-2 focus-visible:outline-brand">
          {!imageFailed && <img src={video.thumbnail_url} alt="" loading="lazy" onError={() => setImageFailed(true)} className="h-full w-full object-cover opacity-80" />}
          <span aria-hidden="true" className="absolute inset-0 flex items-center justify-center text-5xl text-white">▶</span>
        </button>
      )}
      <div className="p-5">
        <p className="text-xs font-semibold uppercase tracking-wide text-brand">{video.category}</p>
        <h3 className="mt-2 text-lg font-semibold leading-snug">{video.title}</h3>
        <p className="mt-3 text-sm text-soft">{video.channel}</p>
        <a href={`https://www.youtube.com/watch?v=${video.video_id}`} target="_blank" rel="noopener noreferrer" className="mt-3 inline-block text-sm font-medium text-brand hover:underline">Watch on YouTube ↗<span className="sr-only"> (opens in a new tab)</span></a>
      </div>
    </article>
  );
}
