from datetime import datetime, timedelta

import pytest
from pydantic import ValidationError

from app.news_state import NewsSnapshot


def test_snapshot_requires_timezone():
    now = datetime(2026, 11, 14, 12)
    with pytest.raises(ValidationError):
        NewsSnapshot(
            articles=[],
            fetched_at=now,
            fresh_until=now + timedelta(hours=6),
            serve_until=now + timedelta(days=1),
        )
