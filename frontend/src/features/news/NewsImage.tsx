import { useState } from "react";

export default function NewsImage({ src, compact = false }: { src: string | null; compact?: boolean }) {
  const [failedSrc, setFailedSrc] = useState<string | null>(null);
  const showImage = !!src && src !== failedSrc;

  return (
    <div className={`relative mb-4 w-full shrink-0 overflow-hidden rounded-lg bg-brand/5 ${compact ? "h-36" : "aspect-video"}`}>
      {showImage ? (
        <img
          src={src}
          alt=""
          width={640}
          height={360}
          loading="lazy"
          referrerPolicy="no-referrer"
          className="absolute inset-0 h-full w-full object-cover"
          onError={() => setFailedSrc(src)}
        />
      ) : (
        <div role="img" aria-label="Article image unavailable" className="flex h-full flex-col items-center justify-center gap-3 bg-gradient-to-br from-brand/10 via-surface to-brand/5 p-4 text-brand">
          <svg aria-hidden="true" viewBox="0 0 64 64" fill="none" className="h-14 w-14 opacity-60" stroke="currentColor" strokeWidth="1.5">
            <rect x="13" y="9" width="38" height="46" rx="5" />
            <path d="M22 20h20M22 27h20M22 44h20" />
            <rect x="22" y="33" width="8" height="5" rx="1" />
            <path d="M35 33h7M35 38h7" />
          </svg>
          <span aria-hidden="true" className="text-[0.65rem] font-semibold uppercase tracking-[0.2em]">Financial news</span>
        </div>
      )}
    </div>
  );
}
