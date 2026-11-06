import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test("shows loading while news is being fetched", () => {
  vi.stubGlobal("fetch", vi.fn(() => new Promise(() => {})));
  render(<FinancialNews />);
  expect(screen.getByRole("status")).toHaveTextContent("Loading financial news");
});
