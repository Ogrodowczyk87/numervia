import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("explains stale results while retaining playable cards", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...videoFeed, stale: true }))));
  render(<FinancialVideos />);
  expect(await screen.findByText(/Showing previously fetched videos/)).toBeVisible();
  expect(screen.getByRole("button", { name: "Play Finance explained" })).toBeVisible();
});
