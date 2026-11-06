from unittest.mock import AsyncMock

import httpx
from fastapi.testclient import TestClient

from app.main import app
from app.videos import VideoCache


def test_videos_cache(monkeypatch):
    monkeypatch.setattr("app.videos.cache", VideoCache())
    monkeypatch.setenv("YOUTUBE_API_KEY", "test-key")
    items = [
        {
            "id": {"videoId": "abcdefghijk"},
            "snippet": {
                "title": "Finance &amp; economy",
                "channelTitle": "Example",
                "publishedAt": "2026-11-06T12:00:00Z",
                "thumbnails": {"default": {"url": "https://example.com/image.jpg"}},
            },
        }
    ]
    provider = AsyncMock(
        return_value=httpx.Response(
            200,
            json={"items": items},
            request=httpx.Request("GET", "https://example.com"),
        )
    )
    monkeypatch.setattr("app.videos.httpx.AsyncClient.get", provider)
    with TestClient(app) as client:
        first = client.get("/api/v1/videos")
        second = client.get("/api/v1/videos")
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()
    assert len(first.json()["videos"]) == 1  # Deduplicated between categories.
    assert first.json()["videos"][0]["title"] == "Finance & economy"
    assert provider.await_count == 3  # Only the first request queries YouTube.
    assert "test-key" not in first.text
