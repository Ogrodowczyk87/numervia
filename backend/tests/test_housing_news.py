def test_housing_news(
    news_client, news_provider, currents_article, provider_response, monkeypatch
):
    from datetime import datetime

    from app.news import cache

    monkeypatch.setenv("CURRENTS_API_KEY", "housing-test-token")
    currents_article["title"] = "Mortgage rates and property prices"
    news_provider.return_value = provider_response(
        {"status": "ok", "news": [currents_article]}
    )
    response = news_client.get("/api/v1/news?feed=housing")
    assert response.status_code == 200
    assert response.json()[0]["provider"] == "currents"
    args = news_provider.call_args
    assert args.args == ("https://api.currentsapi.services/v2/search",)
    assert args.kwargs["headers"] == {"Authorization": "Bearer housing-test-token"}
    params = args.kwargs["params"]
    assert params["keywords"] == "mortgage"
    assert params["page_size"] == 20
    assert (
        datetime.fromisoformat(params["end_date"])
        - datetime.fromisoformat(params["start_date"])
    ).days == 7
    assert len(cache.providers["currents"].attempts) == 1
    assert len(cache.providers["marketaux"].attempts) == 0
    assert news_client.get("/api/v1/news?feed=housing").json() == response.json()
    news_provider.assert_awaited_once()
