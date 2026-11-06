import os
from pathlib import Path

import httpx
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"

router = APIRouter(prefix="/api/v1", tags=["News"])


class NewsArticle(BaseModel):
    title: str
    url: HttpUrl
    source: str
    published_at: str
    image_url: HttpUrl | None = None


@router.get("/news", response_model=list[NewsArticle])
async def get_news():
    token = (
        os.getenv("MARKETAUX_API_TOKEN", "").strip()
        or (dotenv_values(ENV_PATH).get("MARKETAUX_API_TOKEN") or "").strip()
    )

    if not token:
        raise HTTPException(
            status_code=503,
            detail="News is not configured.",
        )

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                "https://api.marketaux.com/v1/news/all",
                params={
                    "api_token": token,
                    "language": "en",
                    "limit": 3,
                },
            )

        response.raise_for_status()
        articles = response.json()["data"]

        return [
            NewsArticle(
                title=article["title"],
                url=article["url"],
                source=article["source"],
                published_at=article["published_at"],
                image_url=article.get("image_url") or None,
            )
            for article in articles
        ]

    except (
        httpx.HTTPError,
        KeyError,
        TypeError,
        ValueError,
    ) as error:
        raise HTTPException(
            status_code=502,
            detail="News is temporarily unavailable.",
        ) from error
