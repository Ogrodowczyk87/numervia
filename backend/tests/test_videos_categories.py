import httpx
from fastapi.testclient import TestClient

from app.main import app


def test_videos_categories(video_provider):
    def response_for(prefix):
        return httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": {"videoId": prefix + str(index) * 10},
                        "snippet": {
                            "title": "Example",
                            "channelTitle": "Channel",
                            "publishedAt": "2026-11-06T12:00:00Z",
                            "thumbnails": {
                                "default": {"url": "https://example.com/thumb.jpg"}
                            },
                        },
                    }
                    for index in range(3)
                ]
            },
            request=httpx.Request("GET", "https://example.com"),
        )

    video_provider.side_effect = [
        response_for("a"),
        response_for("b"),
        response_for("c"),
    ]
    with TestClient(app) as client:
        response = client.get("/api/v1/videos")
    assert response.status_code == 200
    videos = response.json()["videos"]
    assert len(videos) == 6
    assert [v["category"] for v in videos] == [
        "Finance",
        "Finance",
        "Economy",
        "Economy",
        "Technology",
        "Technology",
    ]
    for call in video_provider.call_args_list:
        assert call.kwargs["params"]["videoEmbeddable"] == "true"
        assert call.kwargs["params"]["relevanceLanguage"] == "en"
