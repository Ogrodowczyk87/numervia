import asyncio

import httpx
import pytest

from app.news_refresh import fetch_live


@pytest.mark.parametrize("status", [301, 401, 402, 403, 429, 500])
def test_news_provider_status(news_provider, provider_response, status):
    news_provider.return_value = provider_response({}, status)
    with pytest.raises(httpx.HTTPStatusError):
        asyncio.run(fetch_live("marketaux", "overview", "test-token"))
    news_provider.assert_awaited_once()
