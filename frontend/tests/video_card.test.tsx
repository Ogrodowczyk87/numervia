import { render, screen, fireEvent } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import VideoCard from "../src/features/videos/VideoCard";

test("loads the YouTube player only when selected", () => {
  const video = { video_id: "abcdefghijk", title: "Finance explained", channel: "Example", thumbnail_url: "https://example.com/image.jpg", published_at: "2026-11-06T12:00:00Z", category: "Finance" as const };
  const onPlay = vi.fn();
  const view = render(<VideoCard video={video} active={false} onPlay={onPlay} />);
  expect(document.querySelector("iframe")).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "Play Finance explained" }));
  expect(onPlay).toHaveBeenCalledOnce();
  view.rerender(<VideoCard video={video} active onPlay={onPlay} />);
  expect(screen.getByTitle("YouTube: Finance explained")).toHaveAttribute("src", "https://www.youtube-nocookie.com/embed/abcdefghijk?autoplay=1");
});
