import { act, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, test, vi } from "vitest";
import Navbar from "../src/components/Navbar";
import { ThemeProvider } from "../src/theme/ThemeProvider";

afterEach(() => {
  localStorage.clear();
  delete document.documentElement.dataset.theme;
});

function systemTheme(dark: boolean) {
  const media = { matches: dark, addEventListener: vi.fn(), removeEventListener: vi.fn() };
  vi.stubGlobal("matchMedia", vi.fn(() => media));
  return media;
}

test("persists a manual choice across mounts", () => {
  systemTheme(true);
  const view = render(<ThemeProvider><Navbar /></ThemeProvider>);
  expect(document.documentElement).toHaveAttribute("data-theme", "dark");
  fireEvent.click(screen.getByRole("button", { name: "Switch to light mode" }));
  expect(document.documentElement).toHaveAttribute("data-theme", "light");
  expect(localStorage.getItem("numervia-theme")).toBe("light");
  view.unmount();
  render(<ThemeProvider><Navbar /></ThemeProvider>);
  expect(document.documentElement).toHaveAttribute("data-theme", "light");
  expect(screen.getByRole("button", { name: "Switch to dark mode" })).toBeInTheDocument();
});

test("follows system changes until the user chooses a theme", () => {
  const media = systemTheme(false);
  render(<ThemeProvider><Navbar /></ThemeProvider>);
  expect(document.documentElement).toHaveAttribute("data-theme", "light");
  const change = media.addEventListener.mock.calls[0][1];
  act(() => { media.matches = true; change(); });
  expect(document.documentElement).toHaveAttribute("data-theme", "dark");
  fireEvent.click(screen.getByRole("button", { name: "Switch to light mode" }));
  act(() => { media.matches = false; change(); });
  act(() => { media.matches = true; change(); });
  expect(document.documentElement).toHaveAttribute("data-theme", "light");
});

test("switches theme even when storage is blocked", () => {
  systemTheme(false);
  vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => { throw new Error("blocked"); });
  vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => { throw new Error("blocked"); });
  render(<ThemeProvider><Navbar /></ThemeProvider>);
  fireEvent.click(screen.getByRole("button", { name: "Switch to dark mode" }));
  expect(document.documentElement).toHaveAttribute("data-theme", "dark");
});
