export default function AdPlaceholder() {
  return (
    <aside aria-label="Example advertising space" className="hidden min-w-0 self-stretch py-16 xl:flex xl:flex-col xl:items-center xl:justify-center xl:gap-8">
      <p className="text-center text-[10px] font-medium uppercase tracking-widest text-soft">
        Advertisement · demo
      </p>
      {["Space for your next idea.", "A clearer financial future."].map((title) => (
        <div key={title} className="relative flex h-[800px] w-[220px] shrink-0 2xl:h-[900px] 2xl:w-[300px] flex-col overflow-hidden rounded-xl border border-dashed border-line bg-surface p-6 text-center 2xl:p-8">
          <div aria-hidden="true" className="absolute -right-16 top-20 h-48 w-48 rounded-full bg-brand/15 blur-2xl" />
          <div aria-hidden="true" className="absolute -left-16 bottom-20 h-48 w-48 rounded-full bg-accent/15 blur-2xl" />
          <p className="relative text-sm font-bold tracking-wide text-brand">NUMERVIA</p>
          <div className="relative my-auto">
            <div aria-hidden="true" className="mx-auto mb-10 flex h-24 w-full max-w-40 items-end gap-3">
              <span className="h-8 flex-1 rounded-t bg-brand/30" />
              <span className="h-12 flex-1 rounded-t bg-brand/50" />
              <span className="h-16 flex-1 rounded-t bg-brand/70" />
              <span className="h-24 flex-1 rounded-t bg-brand" />
            </div>
            <p className="text-3xl font-bold leading-tight 2xl:text-4xl">{title}</p>
            <p className="mt-4 text-base leading-relaxed text-muted">Example banner placement.</p>
          </div>
          <p className="relative border-t border-line pt-4 text-center text-xs text-soft"><span className="2xl:hidden">220 × 800</span><span className="hidden 2xl:inline">300 × 900</span></p>
        </div>
      ))}
    </aside>
  );
}
