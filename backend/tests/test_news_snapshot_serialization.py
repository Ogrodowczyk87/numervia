from datetime import UTC, datetime, timedelta

from app.news.state import NewsSnapshot


def test_news_snapshot_survives_json_serialization():
    fetched_at = datetime(2026, 11, 14, 12, 0, tzinfo=UTC)

    snapshot = NewsSnapshot(
        articles=[],
        fetched_at=fetched_at,
        fresh_until=fetched_at + timedelta(hours=6, minutes=5),
        serve_until=fetched_at + timedelta(hours=24),
    )

    saved_json = snapshot.model_dump_json()
    restored = NewsSnapshot.model_validate_json(saved_json)

    assert restored == snapshot
    assert restored.articles == []
    assert restored.fetched_at.utcoffset() == timedelta(0)
