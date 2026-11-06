import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("shows the empty state without navigation buttons", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...videoFeed, videos: [] }))));
  render(<FinancialVideos />);
  expect(await screen.findByText("No videos available right now.")).toBeVisible();
  expect(screen.queryByRole("button", { name: "Next videos" })).not.toBeInTheDocument();
});
