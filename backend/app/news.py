import asyncio
import math
import os
import time
from collections import deque
from pathlib import Path

import httpx
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException

from app.news_providers import NewsArticle, Provider, parse_articles, request_news

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
router = APIRouter(prefix="/api/v1", tags=["News"])
CACHE_SECONDS = 60 * 60
DAY_SECONDS = 24 * 60 * 60
LIMIT_MESSAGE = "Financial news provider request limit reached. Please try again later."
PROVIDERS: dict[Provider, tuple[str, int]] = {
    "marketaux": ("MARKETAUX_API_TOKEN", 80),
    "currents": ("CURRENTS_API_KEY", 200),
}


class ProviderCache:
    def __init__(self):
        self.articles: list[NewsArticle] | None = None
        self.expires_at = 0.0
        self.retry_at = 0.0
        self.error_status = 502
        self.attempts: deque[float] = deque()
        self.lock = asyncio.Lock()


class NewsCache:
    def __init__(self):
        self.providers = {provider: ProviderCache() for provider in PROVIDERS}


cache = NewsCache()


def provider_error(state: ProviderCache) -> HTTPException:
    return HTTPException(
        status_code=state.error_status,
        detail=LIMIT_MESSAGE
        if state.error_status == 429
        else "News is temporarily unavailable.",
        headers={
            "Retry-After": str(max(1, math.ceil(state.retry_at - time.monotonic())))
        },
    )


async def get_provider_news(provider: Provider, token: str) -> list[NewsArticle]:
    state = cache.providers[provider]
    async with state.lock:
        now = time.monotonic()
        if state.articles is not None and now < state.expires_at:
            return state.articles
        if now < state.retry_at:
            raise provider_error(state)
        while state.attempts and state.attempts[0] <= now - DAY_SECONDS:
            state.attempts.popleft()
        if len(state.attempts) >= PROVIDERS[provider][1]:
            state.error_status = 429
            state.retry_at = state.attempts[0] + DAY_SECONDS
            raise provider_error(state)
        # Reserve before HTTP, including failed requests and timeouts.
        state.attempts.append(now)
        try:
            async with asyncio.timeout(12), httpx.AsyncClient(timeout=10) as client:
                response = await request_news(client, provider, token)
            if response.status_code in (402, 429):
                delay = CACHE_SECONDS
                try:
                    delay = max(delay, int(response.headers.get("Retry-After", "0")))
                except ValueError:
                    pass
                state.error_status = 429
                state.retry_at = time.monotonic() + delay
                raise provider_error(state)
            response.raise_for_status()
            articles = parse_articles(provider, response.json())
        except (httpx.HTTPError, TimeoutError, KeyError, TypeError, ValueError) as error:
            state.error_status = 502
            state.retry_at = time.monotonic() + 5 * 60
            raise provider_error(state) from error
        state.articles = articles
        state.expires_at = time.monotonic() + CACHE_SECONDS
        return articles


@router.get("/news", response_model=list[NewsArticle])
async def get_news():
    values = dotenv_values(ENV_PATH)
    configured = [
        (provider, token)
        for provider, (key, _) in PROVIDERS.items()
        if (token := (os.getenv(key, "").strip() or (values.get(key) or "").strip()))
    ]
    if not configured:
        raise HTTPException(status_code=503, detail="News is not configured.")

    # Fetch providers in parallel; each has a 12-second overall deadline.
    results = await asyncio.gather(
        *(get_provider_news(provider, token) for provider, token in configured),
        return_exceptions=True,
    )
    available = [result for result in results if isinstance(result, list)]
    if not available:
        errors = [result for result in results if isinstance(result, HTTPException)]
        if len(errors) == len(results):
            # A temporary failure must not look like both providers hit their quota.
            raise next((e for e in errors if e.status_code != 429), errors[0])
        raise HTTPException(status_code=502, detail="News is temporarily unavailable.")

    unique = {}
    for articles in available:
        for article in articles:
            key = str(article.url).split("#", 1)[0]
            unique.setdefault(key, article)
    return list(unique.values())
