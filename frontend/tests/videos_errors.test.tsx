import { render, screen, fireEvent, act, waitFor } from "@testing-library/react";
import { test, expect, vi } from "vitest";
import FinancialVideos from "../src/features/videos/FinancialVideos";
import { videoFeed } from "./videoFixture";

test.each([503, 502, "network", "invalid"])("handles feed error %s", async (status) => {
  const fetchMock = vi.fn();
  if (status === "network") fetchMock.mockRejectedValue(new TypeError("offline"));
  else fetchMock.mockResolvedValue(new Response(JSON.stringify(status === "invalid" ? {} : { detail: "error" }), { status: typeof status === "number" ? status : 200 }));
  vi.stubGlobal("fetch", fetchMock);
  render(<FinancialVideos />);
  expect(await screen.findByText(/Videos are temporarily unavailable/)).toBeVisible();
});
