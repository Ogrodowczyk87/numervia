import type { MortgageSimulationResponse } from "./types";

const pounds = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "GBP",
});

function formatMoney(value: string) {
  return pounds.format(Number(value));
}

export default function MortgageSummary({
  result,
}: {
  result: MortgageSimulationResponse;
}) {
  const statistics = [
    ["Regular monthly payment", formatMoney(result.monthly_payment)],
    ["Interest without overpayments", formatMoney(result.baseline.total_interest)],
    ["Interest with overpayments", formatMoney(result.with_overpayment.total_interest)],
    ["Interest saved", formatMoney(result.comparison.interest_saved)],
    ["Time saved", `${result.comparison.months_saved} months`],
  ];

  return (
    <section aria-labelledby="mortgage-results" className="rounded-2xl border border-slate-200 bg-white p-6">
      <h2 id="mortgage-results" className="mb-4 text-xl font-semibold">Results</h2>
      <dl className="space-y-4">
        {statistics.map(([label, value]) => (
          <div key={label}>
            <dt className="text-sm text-slate-600">{label}</dt>
            <dd className="text-lg font-semibold">{value}</dd>
          </div>
        ))}
      </dl>
      <p className="mt-6 text-sm text-slate-600">
        Educational model: fixed interest rate for the full term, with no fees or early repayment charges.
      </p>
    </section>
  );
}
