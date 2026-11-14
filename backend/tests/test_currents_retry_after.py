import asyncio
from datetime import timedelta

import pytest

from app.news_refresh import refresh_feed


@pytest.mark.parametrize("header,hours", [("43200", 12), ("bad", 6)])
def test_currents_retry_after(
    news_provider, provider_response, saved_news, header, hours
):
    from app.news_refresh import fetch_live

    store, now, _ = saved_news
    response = provider_response({}, 429)
    response.headers["Retry-After"] = header
    news_provider.return_value = response

    async def fetch(provider, feed):
        return await fetch_live(provider, feed, "test-token")

    asyncio.run(refresh_feed(store, "currents:overview", now, now, fetch))
    assert store.read().providers["currents"].provider_blocked_until == now + timedelta(
        hours=hours
    )
