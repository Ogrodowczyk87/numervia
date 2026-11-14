import { apiUrl } from "../../config/api";
export type Video = {
  video_id: string;
  title: string;
  channel: string;
  thumbnail_url: string;
  published_at: string;
  category: "Finance" | "Economy" | "Technology";
};
export type VideoFeed = {
  videos: Video[];
  updated_at: string;
  fresh_until: string;
  serve_until: string;
  stale: boolean;
  demo: boolean;
};

export async function getVideos(signal: AbortSignal): Promise<VideoFeed> {
  const response = await fetch(apiUrl("/api/v1/videos"), {
    signal: AbortSignal.any([signal, AbortSignal.timeout(15_000)]),
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error(response.status === 503
      ? "Videos are not available yet. Please try again later."
      : "Unable to load videos. Please try again later.");
  }
  const data = await response.json();
  if (!data || !Array.isArray(data.videos)
    || typeof data.stale !== "boolean" || typeof data.demo !== "boolean"
    || ![data.updated_at, data.fresh_until, data.serve_until].every(
      (value) => typeof value === "string" && Number.isFinite(Date.parse(value)),
    )
    || !(Date.parse(data.updated_at) < Date.parse(data.fresh_until)
      && Date.parse(data.fresh_until) <= Date.parse(data.serve_until))
    || Date.parse(data.serve_until) - Date.parse(data.updated_at) > 86_400_000) {
    throw new Error("Invalid video response.");
  }
  return data;
}
