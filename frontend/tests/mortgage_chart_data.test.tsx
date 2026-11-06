import { render, screen, fireEvent, within, waitFor, act } from "@testing-library/react";
import { expect, test, vi } from "vitest";
import type { ReactNode } from "react";
import MortgageChart from "../src/features/mortgage/MortgageChart";
import { mortgageResult } from "./mortgageFixture";
const { capture } = vi.hoisted(() => ({ capture: vi.fn() }));
vi.mock("recharts", () => ({
  ResponsiveContainer: ({ children }: { children: ReactNode }) => <div>{children}</div>,
  LineChart: ({ children, data }: { children: ReactNode; data: unknown }) => { capture(data); return <div>{children}</div>; },
  CartesianGrid: () => null, Legend: () => null, Line: () => null,
  Tooltip: () => null, XAxis: () => null, YAxis: () => null,
}));

test("plots the initial balance and zero after the shorter scenario ends", () => {
  const result = mortgageResult();
  const view = render(<MortgageChart result={result} />);
  const data = capture.mock.lastCall![0];
  expect(data).toHaveLength(25);
  expect(data[0]).toEqual({ month: 0, baseline: 2400, withOverpayment: 2400 });
  expect(data[1]).toEqual({ month: 1, baseline: 2300, withOverpayment: 2000 });
  expect(data[6].withOverpayment).toBe(0);
  expect(data[7].withOverpayment).toBe(0);
  expect(data[24].baseline).toBe(0);
  result.baseline.schedule = [];
  view.rerender(<MortgageChart result={result} />);
  expect(screen.queryByRole("heading")).not.toBeInTheDocument();
});
