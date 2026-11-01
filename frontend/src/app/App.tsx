import Navbar from "../components/Navbar";
import HomePage from "../pages/HomePage";

export default function App() {
  return (
    <>
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:z-10 focus:bg-white focus:p-4"
      >
        Skip to content
      </a>
      <Navbar />
      <main id="main-content" tabIndex={-1}>
        <HomePage />
      </main>
    </>
  );
}
