import asyncio

import pytest

from app.news.refresh import fetch_live


@pytest.mark.parametrize(
    "payload", [{}, {"data": None}, {"data": [{}]}, {"data": [{"title": "Incomplete"}]}]
)
def test_news_invalid_payload(news_provider, provider_response, payload):
    news_provider.return_value = provider_response(payload)
    with pytest.raises((ValueError, TypeError, KeyError)):
        asyncio.run(fetch_live("marketaux", "overview", "test-token"))
