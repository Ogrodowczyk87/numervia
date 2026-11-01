import { useRef, useState } from "react";
import MortgageForm from "./MortgageForm";
import MortgageSummary from "./MortgageSummary";
import { simulateMortgage } from "./mortgageApi";
import type {
  MortgageSimulationRequest,
  MortgageSimulationResponse,
} from "./types";
import MortgageChart from "./MortgageChart";
import MortgageSchedule from "./MortgageSchedule";

export default function MortgageCalculator() {
  const [result, setResult] = useState<MortgageSimulationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const pending = useRef(false);

  async function handleCalculate(request: MortgageSimulationRequest) {
    if (pending.current) return;
    pending.current = true;
    setIsLoading(true);
    setError("");
    setResult(null);

    try {
      setResult(await simulateMortgage(request));
    } catch (cause) {
      if (cause instanceof Error && cause.name === "TimeoutError") {
        setError("The calculation timed out. Please try again.");
      } else {
        setError(
          cause instanceof TypeError
            ? "Cannot connect to the API. Check that the backend is running."
            : cause instanceof Error
              ? cause.message
              : "An unexpected error occurred.",
        );
      }
    } finally {
      pending.current = false;
      setIsLoading(false);
    }
  }

  return (
    <div className="min-w-0 space-y-6">
      <MortgageForm onCalculate={handleCalculate} isLoading={isLoading} />
      <p role="status" className="text-sm text-slate-600">
        {isLoading ? "Calculating…" : ""}
      </p>
      {error && (
        <p role="alert" className="rounded-lg bg-red-50 p-4 text-red-800">
          {error}
        </p>
      )}
      {result && (
        <>
          <MortgageSummary result={result} />
          <MortgageChart result={result} />
          <MortgageSchedule result={result} />
        </>
      )}
    </div>
  );
}
