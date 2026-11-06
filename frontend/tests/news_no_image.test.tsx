import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test("renders articles without images and tolerates an invalid date", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([{ ...article, image_url: null, published_at: "invalid" }]))));
  render(<FinancialNews />);
  await screen.findByRole("link", { name: /Markets update/ });
  expect(document.querySelector("img")).toBeNull();
  expect(screen.getByText(/Date unavailable/)).toBeVisible();
});
