def test_video_api_reads_without_mutating_state_or_fetching(
    video_client, saved_videos, video_provider
):
    store, _, save = saved_videos
    for category in ("Finance", "Economy", "Technology"):
        save(category)
    before = store.path.read_bytes()
    for _ in range(1000):
        response = video_client.get("/api/v1/videos")
        assert response.status_code == 200
        assert response.json()["videos"] == []
        assert response.json()["demo"] is True
        assert response.json()["stale"] is False
        assert response.headers["Cache-Control"] == "no-store"
    assert store.path.read_bytes() == before
    video_provider.assert_not_awaited()
