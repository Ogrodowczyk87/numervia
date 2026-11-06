import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.parametrize("status", [400, 401, 403, 429, 500])
def test_videos_provider_errors(video_provider, status):
    video_provider.return_value = httpx.Response(
        status, json={}, request=httpx.Request("GET", "https://example.com")
    )
    with TestClient(app) as client:
        first = client.get("/api/v1/videos")
        second = client.get("/api/v1/videos")
    assert first.status_code == 502
    assert second.status_code == 503
    assert video_provider.await_count == 1
    assert "test-youtube-key" not in first.text
