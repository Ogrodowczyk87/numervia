import { lazy, Suspense } from "react";
import { ThemeProvider } from "../theme/ThemeProvider";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import MarketTicker from "../components/MarketTicker";
import HomePage from "../pages/HomePage";

const MortgageCalculatorPage = lazy(() => import("../pages/MortgageCalculatorPage"));
const MarketDataPage = lazy(() => import("../pages/MarketDataPage"));
const TechPage = lazy(() => import("../pages/TechPage"));

export default function App() {
  const pathname = window.location.pathname.replace(/\/$/, "");
  const Page = pathname === "/mortgage-calculator"
    ? MortgageCalculatorPage
    : pathname === "/market-data"
      ? MarketDataPage
      : pathname === "/tech"
        ? TechPage
        : HomePage;

  return (
    <ThemeProvider>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-10 focus:bg-surface focus:p-4"
      >
        Skip to content
      </a>
      <MarketTicker />
      <Navbar />
      <main id="main-content" tabIndex={-1}>
        <Suspense fallback={<p role="status" className="p-8">Loading page…</p>}>
          <Page />
        </Suspense>
      </main>
      <Footer />
    </ThemeProvider>
  );
}
