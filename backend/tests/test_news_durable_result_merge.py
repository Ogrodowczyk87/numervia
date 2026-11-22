import asyncio
from datetime import UTC, datetime, timedelta

from app.news_demo import demo_article
from app.news_refresh import refresh_feed
from app.news_state import NewsSnapshot, NewsState
from app.news_store import FileNewsStore


def test_old_result_cannot_overwrite_newer_reservation(tmp_path):
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(NewsState(mode="demo"))
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    newer = demo_article("marketaux", "overview")

    async def fetch(provider, feed):
        def another_writer(state):
            record = state.feeds["marketaux:overview"]
            record.reservation_id = "newer-reservation"
            record.snapshot = NewsSnapshot(
                articles=[newer],
                fetched_at=now,
                fresh_until=now + timedelta(hours=6),
                serve_until=now + timedelta(days=1),
            )

        FileNewsStore(store.path).update(another_writer)
        return []

    asyncio.run(refresh_feed(store, "marketaux:overview", now, now, fetch))
    assert store.read().feeds["marketaux:overview"].snapshot.articles == [newer]
    assert len(store.read().providers["marketaux"].attempts) == 1
