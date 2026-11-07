const modules = [
  { id: "debt-lab", title: "Debt Lab", description: "Compare paying off your highest-interest debts first with clearing your smallest debts first." },
  { id: "investment-lab", title: "Investment Lab", description: "Explore compound growth, regular contributions and inflation using your own assumptions." },
  { id: "decision-lab", title: "Decision Lab", description: "Compare mortgage overpayments with investing, with clear assumptions and uncertainty." },
  { id: "operations-lab", title: "Finance Operations Lab", description: "A planned module for identifying exceptions and duplicate entries in synthetic invoice data.", optional: false },
];

export default function PlannedModules() {
  return (
    <section aria-labelledby="planned-heading" className="mx-auto max-w-5xl px-4 py-12 sm:py-16">
      <h2 id="planned-heading" className="text-2xl font-bold">What’s next for Numervia</h2>
      <p className="mt-3 max-w-2xl text-muted">Mortgage Lab comes first. These modules are planned for future versions and are not available yet.</p>
      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        {modules.map((module) => (
          <article id={module.id} key={module.id} className="scroll-mt-6 rounded-xl border border-line bg-surface p-6 glass-panel transition-colors hover:border-accent/60">
            <span className="text-xs font-semibold uppercase tracking-wide text-soft">{module.optional ? "Optional future module" : "Planned"}</span>
            <h3 className="mt-2 text-lg font-semibold">{module.title}</h3>
            <p className="mt-3 leading-relaxed text-muted">{module.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
