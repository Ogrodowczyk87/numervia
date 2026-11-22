import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article, newsFeed } from "./newsFixture";

test("replaces a broken image while retaining the article", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(newsFeed([article])))));
  render(<FinancialNews />);
  await screen.findByRole("link", { name: /Markets update/ });
  const image = document.querySelector("img")!;
  fireEvent.error(image);
  expect(image).not.toBeVisible();
  expect(screen.getByRole("img", { name: "Article image unavailable" })).toBeVisible();
  expect(screen.getByRole("link", { name: /Markets update/ })).toBeVisible();
});
