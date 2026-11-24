import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import pytest

from app.news.refresh import refresh_feed
from app.news.state import NewsState
from app.news.store import FileNewsStore


@pytest.mark.parametrize("outcome", [[], TimeoutError(), asyncio.CancelledError()])
def test_refresh_reservation_survives_restart_and_failure(tmp_path, outcome):
    path = tmp_path / "state.json"
    store = FileNewsStore(path)
    store.initialize(NewsState(mode="demo"))
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    fetch = (
        AsyncMock(return_value=outcome)
        if isinstance(outcome, list)
        else AsyncMock(side_effect=outcome)
    )
    try:
        asyncio.run(refresh_feed(store, "marketaux:overview", now, now, fetch))
    except asyncio.CancelledError:
        pass
    restarted = FileNewsStore(path)
    repeated = asyncio.run(
        refresh_feed(restarted, "marketaux:overview", now, now, fetch)
    )
    assert repeated.status == "skipped"
    assert fetch.await_count == 1
    assert len(restarted.read().providers["marketaux"].attempts) == 1
    assert restarted.read().feeds[
        "marketaux:overview"
    ].next_attempt_at == now + timedelta(hours=6)
