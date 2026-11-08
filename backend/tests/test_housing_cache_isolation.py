def test_housing_cache_isolation(
    news_client, news_provider, currents_article, provider_response, monkeypatch
):
    from app.news import cache

    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", "test-token")
    now = [100.0]
    monkeypatch.setattr("app.news.time.monotonic", lambda: now[0])
    housing = {
        **currents_article,
        "title": "Mortgage rates",
        "url": "https://example.com/mortgage",
    }
    news_provider.side_effect = [
        provider_response({"status": "ok", "news": [currents_article]}),
        provider_response({"status": "ok", "news": [housing]}),
        provider_response({"status": "ok", "news": []}),
    ]
    assert (
        news_client.get("/api/v1/news").json()[0]["title"] == currents_article["title"]
    )
    assert (
        news_client.get("/api/v1/news?feed=housing").json()[0]["title"]
        == housing["title"]
    )
    now[0] += 21599
    assert (
        news_client.get("/api/v1/news?feed=housing").json()[0]["title"]
        == housing["title"]
    )
    assert news_provider.await_count == 2
    now[0] += 1
    assert news_client.get("/api/v1/news?feed=housing").json() == []
    assert news_provider.await_count == 3
    assert len(cache.providers["currents"].attempts) == 3
