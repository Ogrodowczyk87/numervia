const fixtureNow = Date.now();

export const videoFeed = {
  videos: [
    { video_id: "abcdefghijk", title: "Finance explained", channel: "Example", thumbnail_url: "https://example.com/image.jpg", published_at: "2026-11-06T12:00:00Z", category: "Finance" },
    { video_id: "lmnopqrstuv", title: "Economy explained", channel: "Example", thumbnail_url: "https://example.com/image.jpg", published_at: "2026-11-06T12:00:00Z", category: "Economy" },
  ], updated_at: new Date(fixtureNow).toISOString(),
  fresh_until: new Date(fixtureNow + 6 * 3_600_000).toISOString(),
  serve_until: new Date(fixtureNow + 24 * 3_600_000).toISOString(),
  stale: false, demo: false,
};
