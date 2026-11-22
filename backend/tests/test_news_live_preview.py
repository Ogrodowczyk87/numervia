import asyncio
from unittest.mock import AsyncMock

import pytest

from app.news_demo import demo_articles
from app.news_preview import prepare_preview
from app.news_state import NewsState
from app.news_store import FileNewsStore


@pytest.mark.parametrize("scenario", ["first", "unconfirmed", "no_permission", "demo", "repeat"])
def test_live_preview_reserves_before_fetch_and_requires_explicit_initialization(tmp_path, scenario):
    from datetime import UTC, datetime

    path, marker = tmp_path / "live.json", tmp_path / "enabled"
    store = FileNewsStore(path)
    if scenario == "demo":
        store.initialize(NewsState(mode="demo"))

    async def fetch(provider, feed, token):
        state = store.read()
        assert len(state.providers[provider].attempts) >= 1
        return demo_articles(provider, feed, datetime.now(UTC))

    fetcher = AsyncMock(side_effect=fetch)
    kwargs = {
        "allow_live": scenario != "no_permission",
        "confirm_quota_ready": scenario != "unconfirmed",
        "path": path,
        "marker": marker,
        "tokens": {"marketaux": "test-token"},
        "fetcher": fetcher,
    }
    if scenario in ("unconfirmed", "no_permission", "demo"):
        with pytest.raises(ValueError):
            asyncio.run(prepare_preview(**kwargs))
        fetcher.assert_not_called()
        assert not marker.exists()
        return

    asyncio.run(prepare_preview(**kwargs))
    assert marker.exists()
    state = store.read()
    assert state.mode == "live"
    assert len(state.providers["marketaux"].attempts) == 1
    assert state.feeds["marketaux:overview"].snapshot is not None
    if scenario == "repeat":
        kwargs["confirm_quota_ready"] = False
        asyncio.run(prepare_preview(**kwargs))
        assert len(store.read().providers["marketaux"].attempts) == 1
    assert fetcher.await_count == 1
