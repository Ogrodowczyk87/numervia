import pytest


@pytest.mark.parametrize(
    "age,status,stale",
    [
        (0, 200, False),
        (6, 200, False),
        (7, 200, True),
        (24, 503, None),
        (25, 503, None),
    ],
)
def test_videos_cache_expiration(
    video_client, saved_videos, video_provider, age, status, stale
):
    for category in ("Finance", "Economy", "Technology"):
        saved_videos[2](category, age_hours=age)
    response = video_client.get("/api/v1/videos")
    assert response.status_code == status
    if status == 200:
        assert response.json()["stale"] is stale
    else:
        assert int(response.headers["Retry-After"]) > 0
    video_provider.assert_not_awaited()
