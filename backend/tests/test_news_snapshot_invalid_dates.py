from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.news.state import NewsSnapshot


@pytest.mark.parametrize(
    "fresh_hours,serve_hours", [(-1, 24), (0, 24), (7, 6), (6, 25)]
)
def test_news_snapshot_rejects_invalid_dates(fresh_hours, serve_hours):
    fetched = datetime(2026, 11, 14, 12, tzinfo=UTC)
    with pytest.raises(ValidationError):
        NewsSnapshot(
            articles=[],
            fetched_at=fetched,
            fresh_until=fetched + timedelta(hours=fresh_hours),
            serve_until=fetched + timedelta(hours=serve_hours),
        )
