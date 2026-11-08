import Logo from "./Logo";

export default function Footer() {
  return (
    <footer className="mt-16 border-t border-line bg-canvas/85 backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-[2fr_1fr_1fr]">
          <div>
            <a href="/" className="inline-flex rounded-lg focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand">
              <Logo />
            </a>
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-muted">
              Finance simulation & operations for a clearer financial future.
              Explore scenarios, understand the numbers and compare your options.
            </p>
          </div>
          <nav aria-label="Footer navigation">
            <h2 className="text-sm font-semibold">Explore</h2>
            <ul className="mt-3 space-y-1 text-sm text-muted">
              {[
                ["/", "Home"],
                ["/mortgage-calculator", "Mortgage Calculator"],
                ["/market-data", "Market Data"],
                ["/tech", "Tech"],
              ].map(([href, label]) => (
                <li key={href}>
                  <a href={href} className="inline-flex min-h-11 items-center rounded hover:text-brand focus-visible:outline-2 focus-visible:outline-brand">{label}</a>
                </li>
              ))}
            </ul>
          </nav>
          <div>
            <h2 className="text-sm font-semibold">Built with</h2>
            <ul className="mt-4 flex flex-wrap gap-2 text-xs text-muted">
              {["Python", "FastAPI", "React", "TypeScript", "Tailwind CSS"].map((name) => (
                <li key={name} className="rounded-lg border border-line bg-surface px-3 py-2">{name}</li>
              ))}
            </ul>
            <p className="mt-5 text-xs leading-relaxed text-soft">An evolving project in financial modelling and software development.</p>
          </div>
        </div>
        <div className="mt-8 flex flex-col gap-3 border-t border-line pt-6 text-xs leading-relaxed text-soft sm:flex-row sm:justify-between">
          <p>© {new Date().getFullYear()} Numervia.</p>
          <p className="max-w-xl">Educational tools, not financial advice. Simulations depend on your assumptions; market data may be delayed.</p>
        </div>
      </div>
    </footer>
  );
}
