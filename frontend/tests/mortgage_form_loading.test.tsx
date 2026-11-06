import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import MortgageForm from "../src/features/mortgage/MortgageForm";

test("disables Calculate while a request is pending", () => {
  const onCalculate = vi.fn();
  render(<MortgageForm onCalculate={onCalculate} isLoading />);
  const button = screen.getByRole("button", { name: "Calculating…" });
  expect(button).toBeDisabled();
  fireEvent.click(button);
  expect(onCalculate).not.toHaveBeenCalled();
});
