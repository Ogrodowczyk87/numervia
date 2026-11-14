import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("labels synthetic video previews without pretending to play YouTube content", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...videoFeed, demo: true }))));
  render(<FinancialVideos />);
  expect(await screen.findByText(/Demo videos · Synthetic previews/)).toBeVisible();
  expect(screen.getAllByText("Demo preview")).toHaveLength(2);
  expect(document.querySelector("time")).toHaveAttribute("datetime", videoFeed.updated_at);
  expect(screen.queryByRole("button", { name: /Play/ })).not.toBeInTheDocument();
  expect(screen.queryByRole("link", { name: /Watch on YouTube/ })).not.toBeInTheDocument();
  expect(document.querySelector("iframe")).toBeNull();
  expect(document.querySelector("img")).toBeNull();
});
