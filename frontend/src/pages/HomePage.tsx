import PlannedModules from "../components/PlannedModules";
import MortgageCalculator from "../features/mortgage/MortgageCalculator";

export default function HomePage() {
  return (
    <>
      <section id="home" className="mx-auto max-w-5xl scroll-mt-6 px-4 py-16 sm:py-24">
        <p className="mb-4 text-sm font-semibold uppercase tracking-widest text-blue-700">
          Explore your financial scenarios
        </p>
        <h1 className="max-w-2xl text-4xl font-bold tracking-tight sm:text-5xl">
          See what a little extra could change.
        </h1>
        <p className="mt-6 max-w-xl text-lg leading-relaxed text-slate-600">
          Compare your mortgage with and without monthly overpayments.
          Explore how much interest you could save and how soon you could be debt-free.
        </p>
        <a
          href="#mortgage"
          className="mt-8 inline-block rounded-lg bg-blue-700 px-6 py-3 font-semibold text-white hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700"
        >
          Try the mortgage calculator
        </a>
        <p className="mt-4 text-sm text-slate-500">
          No account needed. Educational simulations, not financial advice.
        </p>
      </section>

      <section
        id="mortgage"
        aria-labelledby="mortgage-heading"
        className="scroll-mt-6 border-t border-slate-200 bg-slate-100/60 px-4 py-12 sm:py-16"
      >
        <div className="mx-auto max-w-xl">
          <h2 id="mortgage-heading" className="text-2xl font-bold">
            Explore your mortgage
          </h2>
          <p className="mb-6 mt-3 text-slate-600">
            Enter your loan details and compare two repayment scenarios.
          </p>
          <MortgageCalculator />
        </div>
      </section>
      <PlannedModules />
    </>
  );
}
