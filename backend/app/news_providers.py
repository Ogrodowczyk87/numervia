from datetime import UTC, datetime
from typing import Literal
from urllib.parse import urlsplit

import httpx
from pydantic import BaseModel, HttpUrl

Provider = Literal["marketaux", "currents"]


class NewsArticle(BaseModel):
    title: str
    url: HttpUrl
    source: str
    published_at: str
    image_url: HttpUrl | None = None
    provider: Provider = "marketaux"


async def request_news(
    client: httpx.AsyncClient, provider: Provider, token: str
) -> httpx.Response:
    if provider == "marketaux":
        return await client.get(
            "https://api.marketaux.com/v1/news/all",
            params={"api_token": token, "language": "en", "limit": 3},
        )
    return await client.get(
        "https://api.currentsapi.services/v2/latest-news",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "language": "en",
            "category": "economy_business_finance",
            "page_size": 20,
        },
    )


def parse_articles(provider: Provider, payload: dict) -> list[NewsArticle]:
    if not isinstance(payload, dict):
        raise TypeError("Invalid news response")
    if provider == "currents" and payload.get("status") != "ok":
        raise ValueError("Invalid news response")
    entries = payload["data" if provider == "marketaux" else "news"]
    if not isinstance(entries, list) or any(not isinstance(e, dict) for e in entries):
        raise ValueError("Invalid news response")
    if provider == "marketaux":
        return [
            NewsArticle(
                title=entry["title"],
                url=entry["url"],
                source=entry["source"],
                published_at=entry["published_at"],
                image_url=entry.get("image_url") or None,
            )
            for entry in entries[:3]
        ]

    articles = []
    for entry in entries[:20]:
        image = entry.get("image")
        if isinstance(image, str) and image.strip().lower() in ("", "none", "null"):
            image = None
        published = datetime.fromisoformat(entry["published"])
        if published.tzinfo is None:
            raise ValueError("News publication timestamp must include timezone")
        articles.append(
            NewsArticle(
                title=entry["title"],
                url=entry["url"],
                source=urlsplit(entry["url"]).hostname or "",
                published_at=published.astimezone(UTC).isoformat(),
                image_url=image,
                provider="currents",
            )
        )
    return articles
