import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test("renders title, source, date, image and safe publisher link", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify([article]))));
  render(<FinancialNews />);
  const link = await screen.findByRole("link", { name: /Markets update/ });
  expect(link).toHaveAttribute("href", article.url);
  expect(link).toHaveAttribute("target", "_blank");
  expect(link).toHaveAttribute("rel", "noopener noreferrer");
  expect(screen.getByText(/example.com/)).toHaveTextContent("6 Nov 2026");
  expect(document.querySelector("img")).toHaveAttribute("src", article.image_url);
  expect(screen.queryByText(/Recent headlines from external publishers/)).not.toBeInTheDocument();
});
