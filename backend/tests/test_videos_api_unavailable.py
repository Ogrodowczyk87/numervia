import pytest


@pytest.mark.parametrize("failure", ["missing", "corrupt", "empty"])
def test_video_api_unavailable_never_fetches(
    video_client, saved_videos, video_provider, failure
):
    store = saved_videos[0]
    if failure == "missing":
        store.path.unlink()
    elif failure == "corrupt":
        store.path.write_text("private-token")
    response = video_client.get("/api/v1/videos")
    assert response.status_code == 503
    assert response.headers["Cache-Control"] == "no-store"
    assert "private-token" not in response.text
    assert video_client.post("/api/v1/videos/refresh").status_code == 404
    video_provider.assert_not_awaited()
