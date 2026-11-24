from datetime import UTC, datetime, timedelta

import pytest

from app.news.refresh import retry_after


@pytest.mark.parametrize(
    "header,hours",
    [
        (None, 6),
        ("invalid", 6),
        ("1", 6),
        ("43200", 12),
        ("Sat, 14 Nov 2026 20:00:00 GMT", 8),
    ],
)
def test_retry_after_never_shortens_refresh_interval(header, hours):
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    assert retry_after(header, now) == timedelta(hours=hours)
