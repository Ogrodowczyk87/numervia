import asyncio
from concurrent.futures import ProcessPoolExecutor
from datetime import UTC, datetime

from app.news_refresh import refresh_feed
from app.news_state import NewsState
from app.news_store import FileNewsStore


def _refresh(path):
    async def fetch(provider, feed):
        return []

    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    return asyncio.run(
        refresh_feed(FileNewsStore(path), "marketaux:overview", now, now, fetch)
    ).status


def test_two_processes_reserve_only_once(tmp_path):
    path = tmp_path / "state.json"
    store = FileNewsStore(path)
    store.initialize(NewsState(mode="demo"))
    with ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(_refresh, [path, path]))
    assert sorted(results) == ["skipped", "updated"]
    assert len(store.read().providers["marketaux"].attempts) == 1
