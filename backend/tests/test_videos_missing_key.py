from fastapi.testclient import TestClient

from app.main import app


def test_videos_missing_key(video_provider, monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY")
    with TestClient(app) as client:
        response = client.get("/api/v1/videos")
    assert response.status_code == 503
    video_provider.assert_not_awaited()
