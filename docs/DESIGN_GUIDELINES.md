# Numervia — design guidelines

Updated: 7 November 2026.

## Direction

Use the owner-supplied “Numervia: Finanse pełne jasności” image as visual inspiration: midnight navy, turquoise actions, restrained violet highlights, crisp white headings and subtly translucent panels. Build the interface using HTML, React and Tailwind; the reference is not a background screenshot or a source of real financial results.

Preserve the product’s existing news, videos, market ticker and dedicated calculator pages. News remains at the top of Home. Planned modules must be clearly distinguished from available tools. Financial illustrations must be labelled and must never impersonate calculated results.

## Shared tokens

Tokens are defined once in `frontend/src/styles/global.css` with Tailwind `@theme`.

| Token | Value | Purpose |
| --- | --- | --- |
| canvas | #08111f | Page background |
| surface | #111e32 | Cards, navbar controls, forms |
| surface-raised | #192a42 | Table headings, hover states |
| line | #30465f | Borders and separators |
| ink | #f3f6fc | Main text |
| muted | #bccbe0 | Supporting text |
| soft | #9baec7 | Metadata and secondary labels |
| brand | #20e4d0 | Primary buttons, focus, first chart series |
| brand-hover | #6bf3e4 | Primary hover |
| accent | #b68aff | Secondary highlights and second chart series |

Use semantic classes such as `bg-surface`, `text-muted` and `border-line`. Do not redefine the palette in each component. Dark text (`text-canvas`) belongs on bright turquoise buttons. Never use white text on a bright turquoise primary action.

## Layout and components

- Use max-width containers, generous section spacing and responsive horizontal padding.
- Main content headings: bold, compact tracking; body text: relaxed line height.
- Cards: rounded-xl or rounded-2xl, thin borders; `glass-panel` is for introductory and platform cards.
- Gradients and glows are decorative accents, not a background behind dense financial data.
- Navbar retains existing destinations, an identifiable active page and mobile hamburger.
- Forms retain visible labels, input limits, loading and error handling.
- Tables retain stable columns, legible numbers, pagination and internal horizontal scrolling.
- Charts use turquoise and violet, distinct solid/dashed lines, visible axes and dark tooltips. Never communicate meaning through colour alone.
- Third-party widgets keep their own branding. Apply a supported dark theme without hiding attribution.
- Footer describes the product and current stack; do not imply AWS is deployed before it actually is.

## Accessibility and responsive behaviour

- Keep keyboard focus clearly visible in turquoise and provide accessible names.
- Interactive controls should have generous touch targets (normally at least 44px).
- At 320px and above, content stacks naturally; only tables and media strips scroll horizontally.
- Preserve Escape behaviour and `aria-expanded` in the hamburger menu.
- Do not add continuous decorative animation; respect reduced-motion preferences for future animation.
- Text and interactive states should meet WCAG AA contrast; verify new combinations rather than relying on appearance.

## Scope and consistency

Current default is dark mode, using local/system fonts and existing dependencies. Do not introduce a new CSS framework, external font service, icon dependency or light-mode switch without a concrete task.

The decorative wave symbol used in navigation/footer is a temporary text mark, not the final logo asset. Integrating the approved logo is a separate asset task.

Before shipping new designs: run frontend tests and `npm run build`, then inspect desktop/mobile, keyboard focus, chart tooltip, form validation and third-party widget rendering in a browser. Passing tests does not certify visual quality.
