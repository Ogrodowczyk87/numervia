import { fireEvent, render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import NewsImage from "../src/features/news/NewsImage";

test("tries a new publisher image after a previous URL failed", () => {
  const view = render(<NewsImage src="https://example.com/broken.jpg" />);
  fireEvent.error(view.container.querySelector("img")!);
  expect(screen.getByRole("img", { name: "Article image unavailable" })).toBeVisible();

  view.rerender(<NewsImage src="https://example.com/replacement.jpg" />);
  expect(view.container.querySelector("img")).toHaveAttribute("src", "https://example.com/replacement.jpg");
  expect(screen.queryByRole("img", { name: "Article image unavailable" })).not.toBeInTheDocument();
});
