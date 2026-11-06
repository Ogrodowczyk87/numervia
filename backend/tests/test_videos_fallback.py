from datetime import UTC, datetime
from unittest.mock import AsyncMock

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.videos import VideoCache, VideoFeed


def test_videos_fallback(monkeypatch):
    cache = VideoCache()
    cache.feed = VideoFeed(videos=[], updated_at=datetime.now(UTC))
    monkeypatch.setattr("app.videos.cache", cache)
    monkeypatch.setenv("YOUTUBE_API_KEY", "test-key")
    provider = AsyncMock(side_effect=httpx.ConnectError("Unavailable"))
    monkeypatch.setattr("app.videos.httpx.AsyncClient.get", provider)
    with TestClient(app) as client:
        first = client.get("/api/v1/videos")
        second = client.get("/api/v1/videos")
    assert first.status_code == second.status_code == 200
    assert first.json()["stale"] is True
    assert provider.await_count == 1  # Backoff prevents repeated failed requests.
