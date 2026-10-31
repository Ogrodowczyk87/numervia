import type {
  MortgageSimulationRequest,
  MortgageSimulationResponse,
} from "./types";

export async function simulateMortgage(
  request: MortgageSimulationRequest,
): Promise<MortgageSimulationResponse> {
  const response = await fetch("/api/v1/mortgage/simulate", {
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
        "Backend jest niedostępny lub wystąpił błąd serwera. Sprawdź terminal FastAPI (port 8000).",
      );
    }
    if (response.status === 422) {
      throw new Error("Sprawdź dane kredytu — serwer odrzucił żądanie.");
    }

    throw new Error("Nie udało się obliczyć wyniku. Spróbuj ponownie.");
  }

  return response.json();
}
