import asyncio
from unittest.mock import AsyncMock

import pytest

from app.video_cli import demo_video
from app.video_refresh import refresh_category


@pytest.mark.parametrize("invalid", ["wrong_category", "too_many", "bad_payload"])
def test_invalid_video_result_preserves_saved_snapshot_and_spends_attempt(
    saved_videos, invalid
):
    store, now, save = saved_videos
    save(videos=[demo_video("Finance", now)])
    original = store.read().categories["Finance"].snapshot
    results = {
        "wrong_category": [demo_video("Economy", now)],
        "too_many": [demo_video("Finance", now)] * 3,
        "bad_payload": [{}],
    }
    result = asyncio.run(
        refresh_category(
            store, "Finance", now, now, AsyncMock(return_value=results[invalid])
        )
    )
    assert result.status == "provider_error"
    assert store.read().categories["Finance"].snapshot == original
    assert len(store.read().attempts) == 1
    assert store.read().last_error_code == "invalid_data"
