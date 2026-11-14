import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.news_refresh import refresh_feed
from app.news_state import NewsState
from app.news_store import FileNewsStore


@pytest.mark.parametrize("offset,mode", [(-1, "demo"), (301, "demo"), (0, "live")])
def test_delayed_future_or_wrong_mode_never_calls_provider(tmp_path, offset, mode):
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(NewsState(mode="demo"))
    slot = datetime(2026, 11, 14, 12, tzinfo=UTC)
    fetch = AsyncMock(return_value=[])
    if mode == "live":
        with pytest.raises(ValueError):
            asyncio.run(
                refresh_feed(store, "marketaux:overview", slot, slot, fetch, mode=mode)
            )
    else:
        result = asyncio.run(
            refresh_feed(
                store,
                "marketaux:overview",
                slot,
                slot + timedelta(seconds=offset),
                fetch,
            )
        )
        assert result.status == "skipped"
    fetch.assert_not_awaited()
    assert store.read().providers["marketaux"].attempts == []
