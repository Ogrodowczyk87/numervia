import MortgageCalculator from "../features/mortgage/MortgageCalculator";

export default function MortgageCalculatorPage() {
  return (
    <section className="mx-auto max-w-4xl px-4 py-10 sm:py-16">
      <h1 className="text-3xl font-bold">Mortgage Calculator</h1>
      <p className="mb-8 mt-3 text-slate-600">
        Compare repayments, explore monthly overpayments and see how much interest you could save.
      </p>
      <MortgageCalculator />
    </section>
  );
}
