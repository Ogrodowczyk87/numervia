def test_video_api_does_not_need_youtube_key(
    video_client, saved_videos, video_provider, monkeypatch
):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    saved_videos[2]()
    assert video_client.get("/api/v1/videos").status_code == 200
    video_provider.assert_not_awaited()
