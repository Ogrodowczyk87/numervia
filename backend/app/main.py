from fastapi import FastAPI

from app.finance.mortgage import simulate_mortgage
from app.models import MortgageSimulationRequest, MortgageSimulationResponse

app = FastAPI(title="Numervia API")


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/mortgage/simulate", response_model=MortgageSimulationResponse)
def simulate(request: MortgageSimulationRequest) -> MortgageSimulationResponse:
    result = simulate_mortgage(request.to_mortgage_input())
    return MortgageSimulationResponse.model_validate(result)
