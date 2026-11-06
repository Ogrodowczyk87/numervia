import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test("renders an empty state", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("[]")));
  render(<FinancialNews />);
  expect(await screen.findByText("No headlines available right now.")).toBeInTheDocument();
});
