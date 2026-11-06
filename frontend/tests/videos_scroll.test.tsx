import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("scroll buttons move the video strip in both directions", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(videoFeed))));
  render(<FinancialVideos />);
  await screen.findByRole("button", { name: "Play Finance explained" });
  const strip = screen.getByRole("region", { name: "Video selection" });
  const scrollBy = vi.fn();
  Object.defineProperty(strip, "clientWidth", { value: 600 });
  Object.defineProperty(strip, "scrollBy", { value: scrollBy });
  fireEvent.click(screen.getByRole("button", { name: "Next videos" }));
  expect(scrollBy).toHaveBeenLastCalledWith({ left: 600, behavior: "smooth" });
  fireEvent.click(screen.getByRole("button", { name: "Previous videos" }));
  expect(scrollBy).toHaveBeenLastCalledWith({ left: -600, behavior: "smooth" });
});
