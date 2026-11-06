import asyncio
import os
import time
from datetime import UTC, datetime, timedelta
from html import unescape
from pathlib import Path
from typing import Literal

import httpx
from dotenv import dotenv_values
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter(prefix="/api/v1", tags=["Videos"])
ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
CACHE_SECONDS = 6 * 60 * 60
QUERIES = {
    "Finance": "personal finance investing explained",
    "Economy": "economy economics news explained",
    "Technology": "technology innovation news explained",
}


class Video(BaseModel):
    video_id: str = Field(pattern=r"^[A-Za-z0-9_-]{11}$")
    title: str
    channel: str
    thumbnail_url: HttpUrl
    published_at: datetime
    category: Literal["Finance", "Economy", "Technology"]


class VideoFeed(BaseModel):
    videos: list[Video]
    updated_at: datetime
    stale: bool = False


class VideoCache:
    def __init__(self):
        self.feed: VideoFeed | None = None
        self.expires_at = 0.0
        self.retry_at = 0.0
        self.lock = asyncio.Lock()


cache = VideoCache()


@router.get("/videos", response_model=VideoFeed)
async def get_videos() -> VideoFeed:
    async with cache.lock:
        now = time.monotonic()
        if cache.feed is not None and now < cache.expires_at:
            return cache.feed
        if now < cache.retry_at:
            if cache.feed is not None:
                return cache.feed.model_copy(update={"stale": True})
            raise HTTPException(503, "Videos are temporarily unavailable.")

        token = (
            os.getenv("YOUTUBE_API_KEY", "").strip()
            or (dotenv_values(ENV_PATH).get("YOUTUBE_API_KEY") or "").strip()
        )
        if not token:
            raise HTTPException(503, "Videos are not configured yet.")

        try:
            videos = []
            seen = set()
            async with httpx.AsyncClient(timeout=10) as client:
                for category, query in QUERIES.items():
                    response = await client.get(
                        "https://www.googleapis.com/youtube/v3/search",
                        headers={"X-Goog-Api-Key": token},
                        params={
                            "part": "snippet",
                            "type": "video",
                            "q": query,
                            "maxResults": 5,
                            "relevanceLanguage": "en",
                            "safeSearch": "strict",
                            "videoEmbeddable": "true",
                            "videoSyndicated": "true",
                            "order": "relevance",
                            "publishedAfter": (
                                datetime.now(UTC) - timedelta(days=30)
                            ).isoformat(),
                        },
                    )
                    response.raise_for_status()
                    added = 0
                    for item in response.json()["items"]:
                        video_id = item["id"]["videoId"]
                        if video_id in seen:
                            continue
                        snippet = item["snippet"]
                        thumbnails = snippet["thumbnails"]
                        thumbnail = thumbnails.get("high") or thumbnails["default"]
                        videos.append(
                            Video(
                                video_id=video_id,
                                title=unescape(snippet["title"]),
                                channel=unescape(snippet["channelTitle"]),
                                thumbnail_url=thumbnail["url"],
                                published_at=snippet["publishedAt"],
                                category=category,
                            )
                        )
                        seen.add(video_id)
                        added += 1
                        if added == 2:
                            break
            cache.feed = VideoFeed(videos=videos, updated_at=datetime.now(UTC))
            cache.expires_at = time.monotonic() + CACHE_SECONDS
            cache.retry_at = 0
            return cache.feed
        except httpx.HTTPError, KeyError, TypeError, ValueError:
            cache.retry_at = time.monotonic() + 300
            if cache.feed is not None:
                return cache.feed.model_copy(update={"stale": True})
            raise HTTPException(502, "Videos are temporarily unavailable.") from None
