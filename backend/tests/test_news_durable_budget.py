import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.news.refresh import refresh_feed
from app.news.state import Attempt, NewsState
from app.news.store import FileNewsStore


@pytest.mark.parametrize("provider,limit", [("marketaux", 80), ("currents", 200)])
def test_durable_budget_blocks_until_oldest_attempt_expires(tmp_path, provider, limit):
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    state = NewsState(mode="demo")
    state.providers[provider].attempts = [
        Attempt(
            id=str(i),
            provider=provider,
            feed="overview",
            at=now,
            slot=now,
        )
        for i in range(limit)
    ]
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(state)
    fetch = AsyncMock(return_value=[])
    result = asyncio.run(refresh_feed(store, f"{provider}:overview", now, now, fetch))
    assert result.status == "budget_exhausted"
    fetch.assert_not_awaited()
    tomorrow = now + timedelta(days=1)
    result = asyncio.run(
        refresh_feed(store, f"{provider}:overview", tomorrow, tomorrow, fetch)
    )
    assert result.status == "updated"
    assert len(store.read().providers[provider].attempts) == 1
