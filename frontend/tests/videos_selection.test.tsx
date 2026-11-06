import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("switches playback so only the selected player is mounted", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(videoFeed))));
  render(<FinancialVideos />);
  fireEvent.click(await screen.findByRole("button", { name: "Play Finance explained" }));
  expect(screen.getByTitle("YouTube: Finance explained")).toBeVisible();
  fireEvent.click(screen.getByRole("button", { name: "Play Economy explained" }));
  expect(screen.queryByTitle("YouTube: Finance explained")).not.toBeInTheDocument();
  expect(screen.getByTitle("YouTube: Economy explained")).toBeVisible();
  expect(document.querySelectorAll("iframe")).toHaveLength(1);
});
