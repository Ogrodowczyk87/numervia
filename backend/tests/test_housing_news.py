import asyncio
from datetime import datetime

from app.news_refresh import fetch_live


def test_housing_news(news_provider, currents_article, provider_response):
    currents_article["title"] = "Mortgage rates change"
    news_provider.return_value = provider_response(
        {"status": "ok", "news": [currents_article]}
    )
    result = asyncio.run(fetch_live("currents", "housing", "test-token"))
    assert len(result) == 1
    params = news_provider.call_args.kwargs["params"]
    assert params["keywords"] == "mortgage"
    assert params["page_size"] == 20
    assert (
        datetime.fromisoformat(params["end_date"])
        - datetime.fromisoformat(params["start_date"])
    ).days == 7
