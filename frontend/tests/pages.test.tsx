import { render, screen } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import App from "../src/app/App";

vi.mock("../src/features/mortgage/MortgageCalculator", () => ({ default: () => <div data-testid="calculator">Calculator</div> }));

test.each([
  ["/", "Financial news"],
  ["/market-data", "Market Data"],
  ["/market-data/", "Market Data"],
  ["/tech", "Tech"],
  ["/mortgage-calculator", "Mortgage Calculator"],
])("renders the correct page at %s", async (path, heading) => {
  window.history.replaceState({}, "", path);
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("[]")));
  render(<App />);
  expect(await screen.findByRole("heading", { name: heading })).toBeVisible();
  if (path === "/") {
    expect(screen.queryByTestId("calculator")).not.toBeInTheDocument();
    const sections = document.querySelectorAll("main section");
    expect(sections[0]).toHaveAccessibleName("Financial news");
    expect(screen.getByRole("link", { name: "Try the mortgage calculator" })).toHaveAttribute("href", "/mortgage-calculator");
  } else {
    expect(screen.queryByRole("heading", { name: "Financial news" })).not.toBeInTheDocument();
  }
});
