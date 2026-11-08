import re
from datetime import UTC, datetime, timedelta
from typing import Literal
from urllib.parse import urlsplit

import httpx
from pydantic import BaseModel, HttpUrl

Provider = Literal["marketaux", "currents"]
Feed = Literal["overview", "housing"]
HOUSING_HEADLINE = re.compile(
    r"\b(mortgage\w*|real estate|propert(?:y|ies)|housing|house prices?|"
    r"home loans?|homebuy\w*|homeowner\w*|refinanc\w*|landlord\w*|buy.to.let|rents?|rental\w*)\b",
    re.IGNORECASE,
)


def is_housing_headline(title: str) -> bool:
    return bool(HOUSING_HEADLINE.search(title)) and "mortgage import" not in title.lower()


class NewsArticle(BaseModel):
    title: str
    url: HttpUrl
    source: str
    published_at: str
    image_url: HttpUrl | None = None
    provider: Provider = "marketaux"


async def request_news(
    client: httpx.AsyncClient, provider: Provider, token: str, feed: Feed = "overview"
) -> httpx.Response:
    if provider == "marketaux":
        return await client.get(
            "https://api.marketaux.com/v1/news/all",
            params={"api_token": token, "language": "en", "limit": 3},
        )
    if feed == "housing":
        now = datetime.now(UTC)
        return await client.get(
            "https://api.currentsapi.services/v2/search",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "language": "en",
                "keywords": "mortgage",
                "start_date": (now - timedelta(days=7)).isoformat(),
                "end_date": now.isoformat(),
                "page_size": 20,
            },
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
