import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import httpx
import pytest

from app.news_refresh import refresh_feed
from app.news_state import NewsState
from app.news_store import FileNewsStore


@pytest.mark.parametrize("status", [301, 401, 403, 402, 429, 500])
def test_provider_error_keeps_attempt_and_applies_persistent_policy(tmp_path, status):
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(NewsState(mode="demo"))
    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    response = httpx.Response(
        status, request=httpx.Request("GET", "https://example.com")
    )
    fetch = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "provider error", request=response.request, response=response
        )
    )
    result = asyncio.run(refresh_feed(store, "currents:overview", now, now, fetch))
    assert result.status == "provider_error"
    budget = FileNewsStore(store.path).read().providers["currents"]
    assert len(budget.attempts) == 1
    assert budget.provider_disabled is (status in (401, 403))
    if status in (402, 429):
        assert budget.provider_blocked_until == now + timedelta(
            hours=24 if status == 402 else 6
        )
