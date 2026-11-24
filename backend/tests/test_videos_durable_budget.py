import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock

import pytest

from app.videos.refresh import refresh_category
from app.videos.state import VideoAttempt, VideoBudget


@pytest.mark.parametrize("cost,daily", [(1, 100), (100, 10000)])
def test_video_budget_reserves_each_search_and_expires_after_24h(
    saved_videos, cost, daily
):
    store, now, _ = saved_videos

    def fill(state):
        state.budget = VideoBudget(
            daily_quota=daily, cost_per_search=cost, request_budget=80
        )
        state.attempts = [
            VideoAttempt(id=str(i), category="Finance", at=now, slot=now)
            for i in range(79)
        ]

    store.update(fill)
    fetch = AsyncMock(return_value=[])
    assert (
        asyncio.run(refresh_category(store, "Finance", now, now, fetch)).status
        == "updated"
    )
    assert (
        asyncio.run(refresh_category(store, "Economy", now, now, fetch)).status
        == "budget_exhausted"
    )
    fetch.assert_awaited_once()
    tomorrow = now + timedelta(days=1)
    assert (
        asyncio.run(
            refresh_category(store, "Economy", tomorrow, tomorrow, fetch)
        ).status
        == "updated"
    )
    assert len(store.read().attempts) == 1
