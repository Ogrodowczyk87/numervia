def test_news_cache(
    news_client, news_provider, news_article, provider_response, monkeypatch
):
    now = [100.0]
    monkeypatch.setattr("app.news.time.monotonic", lambda: now[0])
    news_provider.return_value = provider_response({"data": [news_article]})
    assert news_client.get("/api/v1/news").json() == [news_article]
    assert news_client.get("/api/v1/news").json() == [news_article]
    assert news_provider.await_count == 1
    now[0] += 3601
    news_provider.return_value = provider_response({"data": []})
    assert news_client.get("/api/v1/news").json() == []
    assert news_client.get("/api/v1/news").json() == []
    assert news_provider.await_count == 2
