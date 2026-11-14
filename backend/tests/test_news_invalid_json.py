import asyncio

import httpx
import pytest

from app.news_refresh import fetch_live


def test_news_invalid_json(news_provider):
    news_provider.return_value = httpx.Response(
        200, text="not json", request=httpx.Request("GET", "https://example.com")
    )
    with pytest.raises(ValueError):
        asyncio.run(fetch_live("marketaux", "overview", "test-token"))
