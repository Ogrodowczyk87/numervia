import asyncio
from datetime import timedelta
from unittest.mock import AsyncMock

import httpx
import pytest

from app.video_refresh import refresh_category


@pytest.mark.parametrize(
    "status,reason,code,disabled,blocked_hours",
    [
        (400, "badRequest", "unavailable", False, None),
        (401, "invalidCredentials", "credentials", True, None),
        (403, "forbidden", "credentials", True, None),
        (403, "quotaExceeded", "quota", False, 24),
        (403, "dailyLimitExceeded", "quota", False, 24),
        (403, "rateLimitExceeded", "rate_limit", False, 6),
        (403, "userRateLimitExceeded", "rate_limit", False, 6),
        (400, "keyInvalid", "credentials", True, None),
        (429, "rateLimitExceeded", "rate_limit", False, 6),
        (500, "backendError", "unavailable", False, None),
    ],
)
def test_videos_provider_errors(
    saved_videos, status, reason, code, disabled, blocked_hours
):
    store, now, _ = saved_videos
    response = httpx.Response(
        status,
        json={"error": {"errors": [{"reason": reason}]}},
        request=httpx.Request("GET", "https://example.com"),
    )
    fetch = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "private-key", request=response.request, response=response
        )
    )
    assert (
        asyncio.run(refresh_category(store, "Finance", now, now, fetch)).status
        == "provider_error"
    )
    assert (
        asyncio.run(refresh_category(store, "Finance", now, now, fetch)).status
        == "skipped"
    )
    state = store.read()
    assert len(state.attempts) == 1
    assert state.last_error_code == code
    assert state.provider_disabled is disabled
    if blocked_hours:
        assert state.provider_blocked_until == now + timedelta(hours=blocked_hours)
    assert "private-key" not in store.path.read_text()
    fetch.assert_awaited_once()
