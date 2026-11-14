import asyncio
from unittest.mock import AsyncMock

import httpx
import pytest

from app.news_refresh import refresh_feed


@pytest.mark.parametrize("provider", ["marketaux", "currents"])
def test_news_failed_attempt_budget(saved_news, provider):
    store, now, _ = saved_news
    fetch = AsyncMock(side_effect=httpx.ConnectError("private-token"))
    for _ in range(2):
        asyncio.run(refresh_feed(store, f"{provider}:overview", now, now, fetch))
    assert len(store.read().providers[provider].attempts) == 1
    fetch.assert_awaited_once()
