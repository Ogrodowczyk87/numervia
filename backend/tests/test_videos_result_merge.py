import asyncio

from app.videos.refresh import refresh_category


def test_old_video_result_never_overwrites_newer_writer(saved_videos):
    store, now, _ = saved_videos

    async def fetch(category):
        store.update(
            lambda state: setattr(state.categories[category], "reservation_id", "newer")
        )
        return []

    result = asyncio.run(refresh_category(store, "Finance", now, now, fetch))
    assert result.status == "superseded"
    assert store.read().categories["Finance"].snapshot is None
    assert len(store.read().attempts) == 1
