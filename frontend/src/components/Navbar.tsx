import { useRef, useState } from "react";

const links = [
  { href: "/", label: "Home" },
  { href: "/mortgage-calculator", label: "Mortgage Calculator" },
  { href: "/market-data", label: "Market Data" },
  { href: "/tech", label: "Tech" },
  { href: "/#debt-lab", label: "Debt Lab", planned: true },
  { href: "/#investment-lab", label: "Investment Lab", planned: true },
  { href: "/#decision-lab", label: "Decision Lab", planned: true },
  { href: "/#operations-lab", label: "Finance Operations", planned: true },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const toggle = useRef<HTMLButtonElement>(null);

  return (
    <header className="border-b border-slate-200 bg-white">
      <nav
        aria-label="Main navigation"
        className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-4 py-5 sm:px-6"
        onKeyDown={(event) => {
          if (event.key === "Escape" && isOpen) {
            setIsOpen(false);
            toggle.current?.focus();
          }
        }}
      >
        <a href="/" onClick={() => setIsOpen(false)} className="text-xl font-bold tracking-tight">
          Numervia
        </a>
        <button
          ref={toggle}
          type="button"
          aria-label={isOpen ? "Close navigation" : "Open navigation"}
          aria-expanded={isOpen}
          aria-controls="navigation-links"
          onClick={() => setIsOpen(!isOpen)}
          className="flex min-h-11 min-w-11 items-center justify-center rounded-lg border border-slate-200 text-slate-700 hover:bg-slate-100 focus-visible:outline-2 focus-visible:outline-blue-700 xl:hidden"
        >
          <svg aria-hidden="true" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            {isOpen ? <path d="m6 6 12 12M6 18 18 6" /> : <path d="M4 6h16M4 12h16M4 18h16" />}
          </svg>
        </button>
        <ul
          id="navigation-links"
          className={`${isOpen ? "flex" : "hidden"} w-full flex-col gap-1 border-t border-slate-100 pt-3 text-sm font-medium xl:flex xl:w-auto xl:flex-row xl:items-center xl:gap-2 xl:border-0 xl:pt-0`}
        >
          {links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                aria-current={window.location.pathname === link.href ? "page" : undefined}
                onClick={() => setIsOpen(false)}
                className="flex min-h-11 items-center gap-2 rounded-lg px-3 py-2 text-slate-600 hover:bg-slate-50 hover:text-blue-700 focus-visible:outline-2 focus-visible:outline-blue-700"
              >
                {link.label}
                {link.planned && <span className="rounded bg-slate-100 px-1.5 py-0.5 text-[10px] font-medium text-slate-500">Planned</span>}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
