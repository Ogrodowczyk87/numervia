from app.video_cli import demo_video


def test_saved_video_feed_deduplicates_and_keeps_available_categories(
    video_client, saved_videos
):
    store, now, save = saved_videos
    video = demo_video("Finance", now)
    save("Finance", [video])
    save("Economy", [video.model_copy(update={"category": "Economy"})])
    save("Technology", age_hours=24)
    result = video_client.get("/api/v1/videos").json()
    assert len(result["videos"]) == 1
    assert result["stale"] is True
    assert result["updated_at"] == now.isoformat().replace("+00:00", "Z")
    assert store.read().categories["Technology"].snapshot is not None
