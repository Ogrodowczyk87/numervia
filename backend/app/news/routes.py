"""Public news API: reads saved snapshots, never fetches from providers."""

import math
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import AwareDatetime, BaseModel

from app.news.preview import LIVE_PATH, PREVIEW_MARKER
from app.news.providers import Feed, NewsArticle
from app.news.refresh import read_feed, slot_at
from app.news.store import FileNewsStore, StateUnavailable

router = APIRouter(prefix="/api/v1", tags=["News"])
DEFAULT_PATH = Path(__file__).resolve().parents[2] / ".local" / "news-demo.json"


class NewsResponse(BaseModel):
    articles: list[NewsArticle]
    feed: Feed
    fetched_at: AwareDatetime
    fresh_until: AwareDatetime
    serve_until: AwareDatetime
    stale: bool
    demo: bool
    preview: bool = False


def get_store() -> FileNewsStore:
    configured = os.getenv("NEWS_STATE_PATH", "").strip()
    if configured:
        return FileNewsStore(Path(configured))
    return FileNewsStore(LIVE_PATH if PREVIEW_MARKER.is_file() else DEFAULT_PATH)


def current_time() -> datetime:
    return datetime.now(UTC)


@router.get("/news", response_model=NewsResponse)
def get_news(
    response: Response,
    store: Annotated[FileNewsStore, Depends(get_store)],
    now: Annotated[datetime, Depends(current_time)],
    feed: Feed = "overview",
) -> dict:
    headers = {"Cache-Control": "no-store"}
    retry_at = slot_at(now) + timedelta(hours=6)
    headers["Retry-After"] = str(max(1, math.ceil((retry_at - now).total_seconds())))
    try:
        result = read_feed(store, feed, now)
    except StateUnavailable as error:
        code = "news_not_configured" if not store.path.exists() else "news_unavailable"
        raise HTTPException(
            status_code=503,
            detail={"code": code, "message": "News is temporarily unavailable."},
            headers=headers,
        ) from error
    except LookupError as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "news_unavailable",
                "message": "News is temporarily unavailable.",
            },
            headers=headers,
        ) from error
    response.headers["Cache-Control"] = "no-store"
    result["preview"] = PREVIEW_MARKER.is_file() and store.path.resolve() == LIVE_PATH.resolve()
    return result
