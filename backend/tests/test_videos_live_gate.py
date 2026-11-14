import asyncio
from unittest.mock import AsyncMock

import pytest

from app.video_refresh import refresh_category


@pytest.mark.parametrize("mode", ["demo", "live"])
def test_live_refresh_requires_separate_state_and_confirmed_budget(saved_videos, mode):
    store, now, _ = saved_videos
    store.update(lambda state: setattr(state, "mode", mode))
    fetch = AsyncMock(return_value=[])
    with pytest.raises(ValueError):
        asyncio.run(refresh_category(store, "Finance", now, now, fetch, mode="live"))
    assert store.read().attempts == []
    fetch.assert_not_awaited()
