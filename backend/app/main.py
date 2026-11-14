import os
from urllib.parse import urlsplit

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.finance.mortgage import simulate_mortgage
from app.models import MortgageSimulationRequest, MortgageSimulationResponse
from app.news import router as news_router
from app.videos import router as videos_router


def allowed_origins() -> list[str]:
    configured = os.getenv(
        "ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    )
    origins = [origin.strip() for origin in configured.split(",") if origin.strip()]
    for origin in origins:
        parsed = urlsplit(origin)
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.hostname
            or parsed.netloc
            != parsed.hostname + (f":{parsed.port}" if parsed.port else "")
            or parsed.path
            or parsed.query
            or parsed.fragment
            or (
                parsed.scheme == "http"
                and parsed.hostname not in ("localhost", "127.0.0.1")
            )
        ):
            raise ValueError(
                "ALLOWED_ORIGINS must contain exact HTTPS origins or local HTTP origins"
            )
    return list(dict.fromkeys(origins))


def create_app() -> FastAPI:
    application = FastAPI(title="Numervia API")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins(),
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )
    application.include_router(news_router)
    application.include_router(videos_router)
    application.add_api_route("/api/v1/health", health, methods=["GET"])
    application.add_api_route(
        "/api/v1/mortgage/simulate",
        simulate,
        methods=["POST"],
        response_model=MortgageSimulationResponse,
    )
    return application


def health():
    return {"status": "ok"}


def simulate(request: MortgageSimulationRequest) -> MortgageSimulationResponse:
    result = simulate_mortgage(request.to_mortgage_input())
    return MortgageSimulationResponse.model_validate(result)


app = create_app()
