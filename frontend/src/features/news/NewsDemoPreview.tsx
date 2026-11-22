export default function NewsDemoPreview({ title }: { title: string }) {
  const property = /mortgage|home|property|overpayment/i.test(title);
  return (
    <div aria-hidden="true" className="relative mb-5 flex aspect-[16/7] items-end overflow-hidden rounded-lg bg-gradient-to-br from-brand/15 via-surface to-brand/5 p-4 text-brand">
      <span className="relative z-10 text-[0.65rem] font-semibold uppercase tracking-[0.2em]">
        {property ? "Property & planning" : "Money & markets"}
      </span>
      <svg viewBox="0 0 240 100" className="absolute right-0 top-0 h-full w-3/4" fill="none">
        {property ? (
          <g stroke="currentColor" strokeWidth="2" opacity="0.45">
            <path d="M75 50 130 12l55 38M88 42v48h84V42M120 90V62h22v28" />
            <path d="M45 90h165M98 55h12v12H98M150 55h12v12h-12" />
          </g>
        ) : (
          <g stroke="currentColor" strokeWidth="2" opacity="0.45">
            <path d="M20 25h200M20 50h200M20 75h200" opacity="0.2" />
            <path d="m20 80 30-18 25 7 30-30 25 10 30-22 25 8 35-25" strokeWidth="3" strokeLinejoin="round" />
          </g>
        )}
      </svg>
    </div>
  );
}
