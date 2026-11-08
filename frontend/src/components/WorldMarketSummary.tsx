import { createElement } from "react";
import { useTheme } from "../theme/ThemeProvider";

export default function WorldMarketSummary() {
  const { theme } = useTheme();

  return (
    <aside
      aria-labelledby="world-market-summary-heading"
      className="min-w-0 px-4 pb-12 lg:py-16"
    >
      <h2 id="world-market-summary-heading" className="text-2xl font-bold">
        World markets
      </h2>
      <div className="mt-6 min-w-0 rounded-xl border border-line bg-surface">
        {createElement("tv-world-market-summary", {
          key: theme,
          theme,
          style: { display: "block", width: "100%", minWidth: 0, height: "560px" },
        })}
      </div>
      <a
        href="https://www.tradingview.com/markets/indices/"
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 inline-block text-sm text-brand hover:underline focus-visible:outline-2 focus-visible:outline-brand"
      >
        View world markets on TradingView ↗
      </a>
    </aside>
  );
}
