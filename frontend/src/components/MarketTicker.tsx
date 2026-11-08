import { createElement } from "react";
import { useTheme } from "../theme/ThemeProvider";

const overviewSymbols = "FOREXCOM:SPXUSD,FOREXCOM:NSXUSD,FOREXCOM:DJI,FX:EURUSD,BITSTAMP:BTCUSD,BITSTAMP:ETHUSD,CMCMARKETS:GOLD";

export default function MarketTicker() {
  const { theme } = useTheme();
  return (
    <section aria-label="Market overview" className="border-b border-line bg-surface">
      <div className="w-full px-4 py-3 sm:px-6">
        <div className="min-w-0 overflow-hidden" aria-label="Overview quotes">
          {createElement("tv-ticker-tape", {
            key: theme,
            symbols: overviewSymbols,
            theme,
            style: { display: "block", width: "100%", minHeight: "80px" },
          })}
        </div>
      </div>
    </section>
  );
}
