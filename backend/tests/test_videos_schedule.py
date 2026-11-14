import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock

import pytest

from app.video_refresh import refresh_category


@pytest.mark.parametrize("seconds", [-1, 301, 3600, 21600])
def test_video_schedule_rejects_future_and_delayed_events(saved_videos, seconds):
    store, slot, _ = saved_videos
    fetch = AsyncMock(return_value=[])
    result = asyncio.run(
        refresh_category(
            store, "Finance", slot, slot + timedelta(seconds=seconds), fetch
        )
    )
    assert result.status == "skipped"
    fetch.assert_not_awaited()
