import httpx
from fastapi.testclient import TestClient

from app.main import app


def test_videos_cache_expiration(video_provider, monkeypatch):
    clock = [100.0]
    monkeypatch.setattr("app.videos.time.monotonic", lambda: clock[0])
    video_provider.return_value = httpx.Response(
        200, json={"items": []}, request=httpx.Request("GET", "https://example.com")
    )
    with TestClient(app) as client:
        assert client.get("/api/v1/videos").status_code == 200
        clock[0] += 6 * 3600 - 1
        assert client.get("/api/v1/videos").status_code == 200
        assert video_provider.await_count == 3
        clock[0] += 1
        assert client.get("/api/v1/videos").status_code == 200
        assert video_provider.await_count == 6
