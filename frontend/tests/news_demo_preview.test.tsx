import { render, screen, within } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article, newsFeed } from "./newsFixture";

test("shows six illustrative demo cards without external publisher links or images", async () => {
  const articles = Array.from({ length: 6 }, (_, i) => ({
    ...article,
    title: `Illustrative market headline ${i}`,
    url: `https://example.com/demo/${i}`,
    provider: "currents" as const,
  }));
  const fetchMock = vi.fn().mockResolvedValue(new Response(JSON.stringify(newsFeed(articles, "overview", { demo: true }))));
  vi.stubGlobal("fetch", fetchMock);
  render(<FinancialNews />);

  await screen.findByText("Illustrative market headline 5");
  const section = screen.getByRole("region", { name: "Financial news" });
  expect(within(section).getAllByRole("article")).toHaveLength(6);
  expect(within(section).getAllByText("Illustrative headline · Demo only")).toHaveLength(6);
  expect(within(section).queryByRole("link")).not.toBeInTheDocument();
  expect(section.querySelector("img")).toBeNull();
  expect(within(section).getByText(/Synthetic headlines/)).toBeVisible();
  expect(fetchMock).toHaveBeenCalledTimes(1);
});
