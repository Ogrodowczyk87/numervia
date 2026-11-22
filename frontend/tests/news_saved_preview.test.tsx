import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article, newsFeed } from "./newsFixture";

test("labels saved real news as preview while keeping publisher links", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(
    newsFeed([article], "overview", { demo: false, preview: true }),
  ))));
  render(<FinancialNews />);

  expect(await screen.findByText(/Saved preview · No automatic updates/)).toBeVisible();
  expect(screen.queryByText(/Synthetic headlines/)).not.toBeInTheDocument();
  expect(screen.queryByText(/Demo only/)).not.toBeInTheDocument();
  expect(screen.getByRole("link", { name: /Markets update/ })).toHaveAttribute("href", article.url);
});
