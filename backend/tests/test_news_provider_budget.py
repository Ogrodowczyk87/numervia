import asyncio
from unittest.mock import AsyncMock

import pytest

from app.news.refresh import refresh_feed
from app.news.state import Attempt


@pytest.mark.parametrize("provider,limit", [("marketaux", 80), ("currents", 200)])
def test_news_provider_budget(saved_news, provider, limit):
    store, now, _ = saved_news

    def fill(state):
        state.providers[provider].attempts = [
            Attempt(id=str(i), provider=provider, feed="overview", at=now, slot=now)
            for i in range(limit)
        ]

    store.update(fill)
    fetch = AsyncMock(return_value=[])
    result = asyncio.run(refresh_feed(store, f"{provider}:overview", now, now, fetch))
    assert result.status == "budget_exhausted"
    fetch.assert_not_awaited()
