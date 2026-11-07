import { useState } from "react";
import type { MortgageSimulationResponse } from "./types";

const PAGE_SIZE = 12;
const pounds = new Intl.NumberFormat("en-GB", {
  style: "currency",
  currency: "GBP",
});
const buttonClassName =
  "min-h-11 rounded-lg border border-line px-4 py-2 text-sm font-medium hover:bg-surface-raised focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand disabled:cursor-not-allowed disabled:opacity-40";

export default function MortgageSchedule({
  result,
}: {
  result: MortgageSimulationResponse;
}) {
  const [scenario, setScenario] = useState<"baseline" | "with_overpayment">("baseline");
  const [page, setPage] = useState(0);
  const schedule = result[scenario].schedule;
  const pageCount = Math.max(1, Math.ceil(schedule.length / PAGE_SIZE));
  const currentPage = Math.min(page, pageCount - 1);
  const start = currentPage * PAGE_SIZE;
  const entries = schedule.slice(start, start + PAGE_SIZE);
  const scenarioLabel = scenario === "baseline" ? "Without overpayments" : "With overpayments";

  return (
    <section aria-labelledby="schedule-heading" className="min-w-0 rounded-2xl border border-line bg-surface p-4 sm:p-6">
      <h2 id="schedule-heading" className="text-xl font-semibold">Repayment schedule</h2>
      <p id="schedule-description" className="mt-2 text-sm text-muted">
        Principal repaid is the capital portion of your regular payment. Overpayments are shown separately. All amounts are in GBP.
      </p>

      <div className="mt-5 flex flex-wrap gap-2" role="group" aria-label="Repayment scenario">
        {([
          ["baseline", "Without overpayments"],
          ["with_overpayment", "With overpayments"],
        ] as const).map(([value, label]) => (
          <button
            key={value}
            type="button"
            aria-pressed={scenario === value}
            onClick={() => { setScenario(value); setPage(0); }}
            className={`${buttonClassName} ${scenario === value ? "border-brand bg-brand/10 text-brand" : "text-muted"}`}
          >
            {label}
          </button>
        ))}
      </div>

      <p className="mt-4 text-xs text-soft sm:hidden">Swipe the table horizontally to see all columns.</p>
      <div
        className="mt-3 max-w-full overflow-x-auto rounded-lg border border-line focus-visible:outline-2 focus-visible:outline-brand"
        role="region"
        aria-label="Monthly repayment details"
        tabIndex={0}
      >
        <table aria-describedby="schedule-description" className="w-full min-w-[680px] text-right text-sm tabular-nums">
          <caption className="sr-only">{scenarioLabel} — page {currentPage + 1} of {pageCount}</caption>
          <thead className="bg-surface-raised text-muted">
            <tr>
              {["Month", "Regular payment", "Interest", "Principal repaid", "Overpayment", "Balance"].map((label) => (
                <th key={label} scope="col" className="whitespace-nowrap px-4 py-3 font-semibold">{label}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {entries.map((entry) => (
              <tr key={entry.month}>
                <th scope="row" className="px-4 py-3 font-medium">{entry.month}</th>
                {[entry.payment, entry.interest, entry.principal_paid, entry.extra_payment, entry.remaining_balance].map((amount, index) => (
                  <td key={index} className="whitespace-nowrap px-4 py-3">{pounds.format(Number(amount))}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {entries.length === 0 && <p className="mt-4 text-sm text-muted">No repayment entries available.</p>}

      <nav aria-label="Schedule pagination" className="mt-4 flex flex-wrap items-center justify-between gap-3">
        <button type="button" className={buttonClassName} disabled={currentPage === 0} onClick={() => setPage(currentPage - 1)}>Previous</button>
        <p role="status" className="text-sm text-muted">
          Page {currentPage + 1} of {pageCount}
          {entries.length > 0 && <span className="block text-xs">Months {entries[0].month}–{entries[entries.length - 1].month}</span>}
        </p>
        <button type="button" className={buttonClassName} disabled={currentPage >= pageCount - 1} onClick={() => setPage(currentPage + 1)}>Next</button>
      </nav>
    </section>
  );
}
