import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from app.news.refresh import refresh_feed
from app.news.state import NewsState
from app.news.store import FileNewsStore, StateUnavailable


@pytest.mark.parametrize(
    "failure", ["missing", "corrupt", "reservation_write", "result_write"]
)
def test_storage_failure_never_bypasses_reservation(tmp_path, monkeypatch, failure):
    path = tmp_path / "state.json"
    store = FileNewsStore(path)
    if failure != "missing":
        store.initialize(NewsState(mode="demo"))
    if failure == "corrupt":
        path.write_text("broken")
    real_write = store._write
    calls = 0

    def failing_write(state):
        nonlocal calls
        calls += 1
        if calls == (2 if failure == "result_write" else 1):
            raise OSError("Disk unavailable")
        real_write(state)

    if "write" in failure:
        monkeypatch.setattr(store, "_write", failing_write)
    fetch = AsyncMock(return_value=[])
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    with pytest.raises(StateUnavailable):
        asyncio.run(refresh_feed(store, "marketaux:overview", now, now, fetch))
    assert fetch.await_count == (1 if failure == "result_write" else 0)
    if failure == "result_write":
        assert len(FileNewsStore(path).read().providers["marketaux"].attempts) == 1
        assert store.read().feeds["marketaux:overview"].snapshot is None
