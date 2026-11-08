def test_housing_shared_budget(
    news_client, news_provider, provider_response, monkeypatch
):
    from app.news import cache

    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", "test-token")
    monkeypatch.setattr("app.news.time.monotonic", lambda: 100.0)
    cache.providers["currents"].attempts.extend([100.0] * 199)
    news_provider.return_value = provider_response({"status": "ok", "news": []})
    assert news_client.get("/api/v1/news").status_code == 200
    assert news_client.get("/api/v1/news?feed=housing").status_code == 429
    assert news_client.get("/api/v1/news").status_code == 200
    assert len(cache.providers["currents"].attempts) == 200
    news_provider.assert_awaited_once()
