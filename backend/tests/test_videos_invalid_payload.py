import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.mark.parametrize("payload", [{}, {"items": None}, {"items": [{}]}])
def test_videos_invalid_payload(video_provider, payload):
    video_provider.return_value = httpx.Response(
        200, json=payload, request=httpx.Request("GET", "https://example.com")
    )
    with TestClient(app) as client:
        assert client.get("/api/v1/videos").status_code == 502
