import asyncio
from unittest.mock import AsyncMock

from app.news.refresh import refresh_feed
from app.news.state import Attempt


def test_housing_shared_budget(saved_news):
    store, now, _ = saved_news

    def fill(state):
        state.providers["currents"].attempts = [
            Attempt(id=str(i), provider="currents", feed="overview", at=now, slot=now)
            for i in range(199)
        ]

    store.update(fill)
    fetch = AsyncMock(return_value=[])
    assert (
        asyncio.run(refresh_feed(store, "currents:overview", now, now, fetch)).status
        == "updated"
    )
    assert (
        asyncio.run(refresh_feed(store, "currents:housing", now, now, fetch)).status
        == "budget_exhausted"
    )
    fetch.assert_awaited_once()
