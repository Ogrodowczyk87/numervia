import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.news_refresh import read_feed, refresh_feed
from app.news_state import NewsState
from app.news_store import FileNewsStore


@pytest.mark.parametrize("hours,expected", [(0, False), (7, True), (24, None)])
def test_read_empty_snapshot_fresh_stale_expired_without_provider_calls(
    tmp_path, hours, expected
):
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(NewsState(mode="demo"))
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    fetch = AsyncMock(return_value=[])
    asyncio.run(refresh_feed(store, "marketaux:overview", now, now, fetch))
    before = store.path.read_bytes()
    restarted = FileNewsStore(store.path)
    if expected is None:
        with pytest.raises(LookupError):
            read_feed(restarted, "overview", now + timedelta(hours=hours))
    else:
        for _ in range(1000):
            response = read_feed(restarted, "overview", now + timedelta(hours=hours))
            assert response["stale"] is expected
            assert response["articles"] == []
            assert response["demo"] is True
    assert store.path.read_bytes() == before
    fetch.assert_awaited_once()
