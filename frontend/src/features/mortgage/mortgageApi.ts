import { apiUrl } from "../../config/api";
import type {
  MortgageSimulationRequest,
  MortgageSimulationResponse,
} from "./types";

export async function simulateMortgage(
  request: MortgageSimulationRequest,
): Promise<MortgageSimulationResponse> {
  const response = await fetch(apiUrl("/api/v1/mortgage/simulate"), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
    signal: AbortSignal.timeout(15_000),
  });

  if (!response.ok) {
    if (response.status >= 500) {
      throw new Error(
        "The calculation service is temporarily unavailable. Please try again later.",
      );
    }
    if (response.status === 422) {
      throw new Error("Sprawdź dane kredytu — serwer odrzucił żądanie.");
    }

    throw new Error("Nie udało się obliczyć wyniku. Spróbuj ponownie.");
  }

  return response.json();
}
