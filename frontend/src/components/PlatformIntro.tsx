export default function PlatformIntro() {
  return (
    <section id="home" className="relative mx-auto grid max-w-7xl gap-10 overflow-hidden px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-2 lg:items-center">
      <div className="relative z-10">
        <p className="mb-5 text-xs font-semibold uppercase tracking-[0.2em] text-brand">Finance simulation & operations</p>
        <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-5xl lg:text-6xl">
          Compare financial scenarios with <span className="brand-gradient">clarity.</span>
        </h1>
        <p className="mt-6 max-w-xl text-lg leading-relaxed text-muted">
          Explore mortgage repayments today. Discover the direction of Numervia’s future tools for debt, investing and finance operations.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <a href="/mortgage-calculator" className="rounded-xl bg-brand px-6 py-3 font-semibold text-canvas shadow-[0_0_30px_#20e4d025] hover:bg-brand-hover focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand">Try the mortgage calculator</a>
          <a href="#planned-heading" className="rounded-xl border border-line bg-surface px-6 py-3 font-semibold hover:border-accent focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand">Explore roadmap →</a>
        </div>
        <p className="mt-5 text-sm text-soft">No account needed. Educational simulations, not financial advice.</p>
      </div>
      <div className="relative py-5" aria-hidden="true">
        <div className="absolute inset-8 rounded-full bg-brand/10 blur-3xl" />
        <div className="glass-panel relative rounded-3xl p-6 sm:p-8">
          <p className="text-sm font-semibold text-muted">Mortgage Lab</p>
          <p className="mt-2 text-2xl font-semibold">Your choices. A clearer picture.</p>
          <svg viewBox="0 0 440 180" className="mt-6 w-full" fill="none">
            <path d="M0 40H440M0 95H440M0 150H440" stroke="var(--color-line)" strokeDasharray="4 6" />
            <path d="M8 20C120 40 240 75 430 165" stroke="var(--color-accent)" strokeWidth="3" />
            <path d="M8 20C90 50 180 100 290 165H430" stroke="var(--color-brand)" strokeWidth="3" />
          </svg>
          <div className="mt-5 flex flex-wrap gap-3 text-xs text-muted">
            <span className="rounded-lg border border-line px-3 py-2">Compare repayments</span>
            <span className="rounded-lg border border-brand/40 bg-brand/10 px-3 py-2 text-brand">Explore overpayments</span>
          </div>
          <p className="mt-4 text-xs text-soft">Illustration · Calculate to see your actual scenario</p>
        </div>
      </div>
    </section>
  );
}
