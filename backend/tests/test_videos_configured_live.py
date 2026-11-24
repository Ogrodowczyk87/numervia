import asyncio
from unittest.mock import AsyncMock

from app.videos.refresh import refresh_category
from app.videos.state import VideoBudget


def test_configured_live_budget_is_persisted_and_each_search_is_counted(saved_videos):
    store, now, _ = saved_videos

    def configure(state):
        state.mode = "live"
        state.budget = VideoBudget(
            daily_quota=100, cost_per_search=1, request_budget=12
        )
        state.quota_confirmed_at = now

    store.update(configure)
    fetch = AsyncMock(return_value=[])
    for category in ("Finance", "Economy", "Technology"):
        assert (
            asyncio.run(
                refresh_category(store, category, now, now, fetch, mode="live")
            ).status
            == "updated"
        )
    state = store.read()
    assert state.budget.request_budget == 12
    assert len(state.attempts) == 3
    assert state.quota_confirmed_at == now
    assert fetch.await_count == 3
