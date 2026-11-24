import asyncio

import pytest

from app.news.refresh import fetch_live


@pytest.mark.parametrize("image", [None, "", "missing"])
def test_news_optional_image(news_provider, news_article, provider_response, image):
    if image == "missing":
        news_article.pop("image_url")
    else:
        news_article["image_url"] = image
    news_provider.return_value = provider_response({"data": [news_article]})
    result = asyncio.run(fetch_live("marketaux", "overview", "test-token"))
    assert result[0].image_url is None
