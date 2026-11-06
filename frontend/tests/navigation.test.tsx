import { render, screen, fireEvent } from "@testing-library/react";
import { expect, test } from "vitest";
import Navbar from "../src/components/Navbar";

test("navigation links target pages and hamburger closes with Escape", () => {
  window.history.replaceState({}, "", "/tech");
  render(<Navbar />);
  expect(screen.getByRole("link", { name: "Tech" })).toHaveAttribute("aria-current", "page");
  for (const [name, href] of [["Market Data", "/market-data"], ["Mortgage Calculator", "/mortgage-calculator"], ["Tech", "/tech"]]) {
    expect(screen.getByRole("link", { name })).toHaveAttribute("href", href);
  }
  const button = screen.getByRole("button", { name: "Open navigation" });
  fireEvent.click(button);
  expect(button).toHaveAttribute("aria-expanded", "true");
  fireEvent.keyDown(button, { key: "Escape" });
  expect(button).toHaveAttribute("aria-expanded", "false");
  expect(button).toHaveFocus();
  fireEvent.click(button);
  const techLink = screen.getByRole("link", { name: "Tech" });
  techLink.addEventListener("click", (event) => event.preventDefault());
  fireEvent.click(techLink);
  expect(button).toHaveAttribute("aria-expanded", "false");
});
