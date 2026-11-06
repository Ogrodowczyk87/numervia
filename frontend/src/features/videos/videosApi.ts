export type Video = {
  video_id: string;
  title: string;
  channel: string;
  thumbnail_url: string;
  published_at: string;
  category: "Finance" | "Economy" | "Technology";
};
export type VideoFeed = { videos: Video[]; updated_at: string; stale: boolean };

export async function getVideos(signal: AbortSignal): Promise<VideoFeed> {
  const response = await fetch("/api/v1/videos", {
    signal: AbortSignal.any([signal, AbortSignal.timeout(40_000)]),
  });
  if (!response.ok) {
    throw new Error(response.status === 503
      ? "Videos are not available yet. Please try again later."
      : "Unable to load videos. Please try again later.");
  }
  const data = await response.json();
  if (!data || !Array.isArray(data.videos)) {
    throw new Error("Invalid video response.");
  }
  return data;
}
