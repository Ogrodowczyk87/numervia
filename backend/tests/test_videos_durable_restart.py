import asyncio
from unittest.mock import AsyncMock

import pytest

from app.video_refresh import refresh_category
from app.video_store import FileVideoStore


@pytest.mark.parametrize("error", [None, TimeoutError(), asyncio.CancelledError()])
def test_video_reservation_survives_restart_and_crash(saved_videos, error):
    store, now, _ = saved_videos
    fetch = AsyncMock(side_effect=error) if error else AsyncMock(return_value=[])
    try:
        asyncio.run(refresh_category(store, "Finance", now, now, fetch))
    except asyncio.CancelledError:
        pass
    restarted = FileVideoStore(store.path)
    assert (
        asyncio.run(refresh_category(restarted, "Finance", now, now, fetch)).status
        == "skipped"
    )
    assert len(restarted.read().attempts) == 1
    fetch.assert_awaited_once()
