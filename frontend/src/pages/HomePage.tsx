import FinancialNews from "../features/news/FinancialNews";
import PlannedModules from "../components/PlannedModules";

export default function HomePage() {
  return (
    <>
      <FinancialNews />
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
          href="/mortgage-calculator"
          className="mt-8 inline-block rounded-lg bg-blue-700 px-6 py-3 font-semibold text-white hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700"
        >
          Try the mortgage calculator
        </a>
        <p className="mt-4 text-sm text-slate-500">
          No account needed. Educational simulations, not financial advice.
        </p>
      </section>

      <PlannedModules />
    </>
  );
}
