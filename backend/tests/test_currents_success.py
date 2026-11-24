import asyncio

import pytest

from app.news.refresh import fetch_live


@pytest.mark.parametrize(
    "image", [None, "", "None", "null", "https://example.com/a.jpg"]
)
def test_currents_success(news_provider, currents_article, provider_response, image):
    currents_article["image"] = image
    news_provider.return_value = provider_response(
        {"status": "ok", "news": [currents_article]}
    )
    result = asyncio.run(fetch_live("currents", "overview", "test-token"))
    assert result[0].provider == "currents"
    assert result[0].source == "publisher.example"
    assert bool(result[0].image_url) is (image == "https://example.com/a.jpg")
    assert news_provider.call_args.kwargs["headers"] == {
        "Authorization": "Bearer test-token"
    }
