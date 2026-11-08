import { render, screen, within, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test("halves general news and shows two housing cards on mobile from separate cached feeds", async () => {
  const general = Array.from({ length: 20 }, (_, i) => ({ ...article, title: `General headline ${i}`, url: `${article.url}/general/${i}` }));
  const housing = Array.from({ length: 6 }, (_, i) => ({ ...article, title: `Mortgage headline ${i}`, url: `${article.url}/housing/${i}` }));
  const fetchMock = vi.fn((url: string) => Promise.resolve(new Response(JSON.stringify(url.includes("feed=housing") ? housing : general))));
  vi.stubGlobal("fetch", fetchMock);
  render(<FinancialNews sidebar={<aside aria-label="World markets">Market widget</aside>} />);
  await screen.findByRole("link", { name: /Mortgage headline 0/ });
  const main = screen.getByRole("region", { name: "Financial news" });
  const extra = screen.getByRole("region", { name: "Property & mortgages" });
  expect(within(main).getAllByRole("article")).toHaveLength(10);
  expect(within(extra).getAllByRole("article")).toHaveLength(2);
  expect(screen.getByRole("complementary", { name: "World markets" }).compareDocumentPosition(extra) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  expect(fetchMock).toHaveBeenCalledTimes(2);
});

test("keeps the main news visible when housing news fails", async () => {
  vi.stubGlobal("fetch", vi.fn((url: string) => Promise.resolve(url.includes("feed=housing")
    ? new Response("{}", { status: 502 }) : new Response(JSON.stringify([article])))));
  render(<FinancialNews sidebar={<aside>Market widget</aside>} />);
  expect(await screen.findByRole("link", { name: /Markets update/ })).toBeInTheDocument();
  expect(await screen.findByText("Housing news is temporarily unavailable. Please try again later.")).toBeInTheDocument();
});

test("does not repeat general articles inside the housing feed", async () => {
  vi.stubGlobal("fetch", vi.fn().mockImplementation(() => Promise.resolve(new Response(JSON.stringify([article])))));
  render(<FinancialNews sidebar={<aside>Market widget</aside>} />);
  await screen.findByText("No housing headlines available right now.");
  await waitFor(() => expect(screen.getAllByRole("article")).toHaveLength(1));
});
