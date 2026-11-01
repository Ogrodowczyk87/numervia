import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { MortgageSimulationResponse } from "./types";

type MortgageChartProps = {
  result: MortgageSimulationResponse;
};

const pounds = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "GBP",
  maximumFractionDigits: 0,
});

export default function MortgageChart({ result }: MortgageChartProps) {
  const baseline = result.baseline.schedule;
  const overpayment = result.with_overpayment.schedule;

  const firstMonth = baseline[0];

  if (!firstMonth) return null;

  const initialBalance =
    Number(firstMonth.remaining_balance) +
    Number(firstMonth.principal_paid);

  const chartData = [
    {
      month: 0,
      baseline: initialBalance,
      withOverpayment: initialBalance,
    },
    ...baseline.map((entry, index) => ({
      month: entry.month,
      baseline: Number(entry.remaining_balance),
      withOverpayment: Number(
        overpayment[index]?.remaining_balance ?? "0.00",
      ),
    })),
  ];

  return (
    <section
      aria-labelledby="balance-chart-heading"
      className="min-w-0 rounded-2xl border border-slate-200 bg-white p-4 sm:p-6"
    >
      <h2
        id="balance-chart-heading"
        className="text-xl font-semibold"
      >
        Mortgage balance over time
      </h2>

      <p className="mt-2 text-sm text-slate-600">
        Compare your remaining balance with and without overpayments.
      </p>

      <div className="mt-6 h-80 w-full min-w-0">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 10, right: 10, bottom: 10, left: 0 }}
            accessibilityLayer
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} />

            <XAxis
              dataKey="month"
              type="number"
              domain={["dataMin", "dataMax"]}
              tickFormatter={(month: number) => `${month}m`}
              minTickGap={30}
            />

            <YAxis
              width={65}
              tickFormatter={(value: number) =>
                pounds.format(value)
              }
            />

            <Tooltip
              labelFormatter={(month) => `Month ${month}`}
              formatter={(value) =>
                pounds.format(Number(value))
              }
            />

            <Legend />

            <Line
              type="linear"
              dataKey="baseline"
              name="Without overpayments"
              stroke="#2563eb"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
            />

            <Line
              type="linear"
              dataKey="withOverpayment"
              name="With overpayments"
              stroke="#15803d"
              strokeWidth={2}
              strokeDasharray="6 4"
              dot={false}
              isAnimationActive={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <p className="mt-3 text-sm text-slate-600">
        Without overpayments: {result.baseline.months_to_payoff} months.
        {" "}With overpayments: {result.with_overpayment.months_to_payoff} months.
      </p>
    </section>
  );
}