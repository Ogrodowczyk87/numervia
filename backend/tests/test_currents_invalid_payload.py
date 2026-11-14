import asyncio

import pytest

from app.news_refresh import fetch_live


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"status": "error", "news": []},
        {"status": "ok", "news": {}},
        {"status": "ok", "news": [None]},
        {"status": "ok", "news": [{"title": "Incomplete"}]},
    ],
)
def test_currents_invalid_payload(news_provider, provider_response, payload):
    news_provider.return_value = provider_response(payload)
    with pytest.raises((ValueError, TypeError, KeyError)):
        asyncio.run(fetch_live("currents", "overview", "test-token"))
