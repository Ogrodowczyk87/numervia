import argparse
import asyncio
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from app.news.cli import run
from app.news.refresh import read_feed
from app.news.state import NewsState
from app.news.store import FileNewsStore


@pytest.mark.parametrize("existing_mode", [None, "demo", "live"])
def test_preview_is_offline_and_never_overwrites_live_state(tmp_path, monkeypatch, existing_mode):
    path = tmp_path / "news.json"
    store = FileNewsStore(path)
    if existing_mode:
        store.initialize(NewsState(mode=existing_mode))
    before = path.read_bytes() if path.exists() else None
    network = AsyncMock(side_effect=AssertionError("Demo must never use HTTP"))
    monkeypatch.setattr("httpx.AsyncClient.request", network)
    args = argparse.Namespace(path=path, command="preview-demo")

    if existing_mode == "live":
        with pytest.raises(ValueError, match="demo state"):
            asyncio.run(run(args))
        assert path.read_bytes() == before
    else:
        asyncio.run(run(args))
        first = store.read()
        asyncio.run(run(args))
        state = store.read()
        assert state.providers == first.providers
        now = datetime.now(UTC)
        overview = read_feed(store, "overview", now)
        housing = read_feed(store, "housing", now)
        assert overview["demo"] and housing["demo"]
        assert len(overview["articles"]) == 6
        assert len({a["title"] for a in overview["articles"]}) == 6
        assert len(housing["articles"]) == 4
        assert not any(p.attempts for p in state.providers.values())
    network.assert_not_called()
