import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article, newsFeed } from "./newsFixture";

test.each(["currents", "marketaux"])("shows publisher and %s attribution", async (provider) => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(newsFeed([{ ...article, provider: provider as "currents" | "marketaux" }])))));
  render(<FinancialNews />);
  const name = provider === "currents" ? "Currents" : "Marketaux";
  expect(await screen.findByText(new RegExp(`via ${name}`))).toHaveTextContent("example.com");
  if (provider === "currents") {
    expect(screen.getByRole("link", { name: /Powered by Currents News API/ })).toHaveAttribute("href", "https://currentsapi.services/");
  }
  expect(screen.getByRole("link", { name: /Markets update/ })).toHaveAttribute("href", article.url);
});
