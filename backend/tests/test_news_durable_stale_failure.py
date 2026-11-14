import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

from app.news_refresh import read_feed, refresh_feed
from app.news_state import NewsState
from app.news_store import FileNewsStore


def test_failed_refresh_preserves_last_good_snapshot(tmp_path):
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(NewsState(mode="demo"))
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    asyncio.run(
        refresh_feed(store, "marketaux:overview", now, now, AsyncMock(return_value=[]))
    )
    later = now + timedelta(hours=6)
    asyncio.run(
        refresh_feed(
            store,
            "marketaux:overview",
            later,
            later,
            AsyncMock(side_effect=TimeoutError()),
        )
    )
    result = read_feed(store, "overview", later + timedelta(minutes=6))
    assert result["stale"] is True
    assert result["fetched_at"] == now.isoformat()
    assert len(store.read().providers["marketaux"].attempts) == 2
