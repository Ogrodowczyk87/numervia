import { createElement, useState } from "react";

const markets = {
  Overview: "FOREXCOM:SPXUSD,FOREXCOM:NSXUSD,FOREXCOM:DJI,FX:EURUSD,BITSTAMP:BTCUSD,BITSTAMP:ETHUSD,CMCMARKETS:GOLD",
  "US Markets": "FOREXCOM:SPXUSD,FOREXCOM:NSXUSD,FOREXCOM:DJI",
  Cryptocurrencies: "BITSTAMP:BTCUSD,BITSTAMP:ETHUSD",
  Currencies: "FX:GBPUSD,FX:GBPEUR,FX:EURUSD,FX:USDJPY",
  Commodities: "CMCMARKETS:GOLD",
};

export default function MarketTicker() {
  const [market, setMarket] = useState<keyof typeof markets>("Overview");
  return (
    <section aria-label="Market overview" className="border-b border-line bg-surface">
      <div className="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-3 sm:flex-row sm:items-center sm:px-6">
        <div className="shrink-0">
          <label htmlFor="market-selection" className="sr-only">Select market</label>
          <select id="market-selection" value={market} onChange={(event) => setMarket(event.target.value as keyof typeof markets)} className="min-h-11 max-w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm font-semibold focus-visible:outline-2 focus-visible:outline-brand">
            {Object.keys(markets).map((name) => <option key={name}>{name}</option>)}
          </select>
        </div>
        <div className="min-w-0 flex-1 overflow-hidden" aria-label={`${market} quotes`}>
          {createElement("tv-ticker-tape", {
            key: market,
            symbols: markets[market],
            theme: "dark",
            style: { display: "block", width: "100%", minHeight: "80px" },
          })}
        </div>
      </div>
    </section>
  );
}
