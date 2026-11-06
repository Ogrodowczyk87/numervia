import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import FinancialNews from "../src/features/news/FinancialNews";
import { article } from "./newsFixture";

test.each([new TypeError("Network unavailable"), new DOMException("Timeout", "TimeoutError")])("handles network and timeout failures", async (error) => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(error));
  render(<FinancialNews />);
  await waitFor(() => expect(screen.getByRole("status")).not.toHaveTextContent("Loading"));
  expect(screen.getByRole("status")).not.toBeEmptyDOMElement();
  expect(screen.queryByRole("article")).not.toBeInTheDocument();
});
