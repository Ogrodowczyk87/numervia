import { expect, test, vi } from "vitest";
import { getVideos } from "../src/features/videos/videosApi";
import { videoFeed } from "./videoFixture";

test.each([
  { ...videoFeed, updated_at: "invalid" },
  { ...videoFeed, serve_until: videoFeed.updated_at },
  { ...videoFeed, fresh_until: null },
  { ...videoFeed, demo: undefined },
  { ...videoFeed, serve_until: new Date(Date.parse(videoFeed.updated_at) + 25 * 3_600_000).toISOString() },
])("rejects a video feed with invalid lifetime metadata", async (payload) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(payload))));
  await expect(getVideos(new AbortController().signal)).rejects.toThrow("Invalid video response");
});
