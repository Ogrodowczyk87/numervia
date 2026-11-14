import asyncio

from app.video_refresh import fetch_live


def test_videos_categories(video_provider, provider_response, saved_videos):
    videos = []
    for category, prefix in zip(
        ("Finance", "Economy", "Technology"), ("a", "b", "c"), strict=True
    ):
        items = [
            {
                "id": {"videoId": prefix + str(i) * 10},
                "snippet": {
                    "title": "Finance &amp; economy",
                    "channelTitle": "Channel",
                    "publishedAt": "2026-11-06T12:00:00Z",
                    "thumbnails": {"default": {"url": "https://example.com/thumb.jpg"}},
                },
            }
            for i in range(3)
        ]
        video_provider.return_value = provider_response({"items": items})
        videos.extend(asyncio.run(fetch_live(category, "test-key", saved_videos[1])))
    assert len(videos) == 6
    assert [v.category for v in videos] == [
        "Finance",
        "Finance",
        "Economy",
        "Economy",
        "Technology",
        "Technology",
    ]
    assert videos[0].title == "Finance & economy"
    assert video_provider.await_count == 3
    for call in video_provider.call_args_list:
        assert call.kwargs["params"]["videoEmbeddable"] == "true"
        assert call.kwargs["params"]["maxResults"] == 5
