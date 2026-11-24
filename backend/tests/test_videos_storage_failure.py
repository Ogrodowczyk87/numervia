import asyncio
from unittest.mock import AsyncMock

import pytest

from app.videos.refresh import refresh_category
from app.videos.store import VideoStateUnavailable


@pytest.mark.parametrize(
    "failure", ["missing", "corrupt", "reserve_write", "result_write"]
)
def test_video_storage_failure_never_bypasses_durable_budget(
    saved_videos, monkeypatch, failure
):
    store, now, _ = saved_videos
    if failure == "missing":
        store.path.unlink()
    elif failure == "corrupt":
        store.path.write_text("broken")
    actual = store._write
    writes = 0

    def write(state):
        nonlocal writes
        writes += 1
        if writes == (2 if failure == "result_write" else 1):
            raise OSError("disk failure")
        actual(state)

    if "write" in failure:
        monkeypatch.setattr(store, "_write", write)
    fetch = AsyncMock(return_value=[])
    with pytest.raises(VideoStateUnavailable):
        asyncio.run(refresh_category(store, "Finance", now, now, fetch))
    assert fetch.await_count == (1 if failure == "result_write" else 0)
    if failure == "result_write":
        assert len(store.read().attempts) == 1
        assert store.read().categories["Finance"].snapshot is None
