import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock

from app.videos.refresh import refresh_category


def test_videos_fallback(video_client, saved_videos):
    store, now, save = saved_videos
    save(age_hours=7)
    before = store.read().categories["Finance"].snapshot
    result = asyncio.run(
        refresh_category(
            store, "Finance", now, now, AsyncMock(side_effect=TimeoutError())
        )
    )
    assert result.status == "provider_error"
    assert store.read().categories["Finance"].snapshot == before
    assert len(store.read().attempts) == 1
    assert store.read().categories["Finance"].next_attempt_at == now + timedelta(
        hours=6
    )
    assert video_client.get("/api/v1/videos").json()["stale"] is True
