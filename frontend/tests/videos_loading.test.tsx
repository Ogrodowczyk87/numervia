import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test("shows loading while awaiting the feed", () => {
  vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
  render(<FinancialVideos />);
  expect(screen.getByRole("status")).toHaveTextContent("Loading videos");
});
