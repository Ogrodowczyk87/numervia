import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test("hides a broken image while retaining the article", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([article]))));
  render(<FinancialNews />);
  await screen.findByRole("link", { name: /Markets update/ });
  const image = document.querySelector("img")!;
  fireEvent.error(image);
  expect(image).not.toBeVisible();
  expect(screen.getByRole("link", { name: /Markets update/ })).toBeVisible();
});
