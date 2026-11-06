def test_news_missing_token(news_client, news_provider, monkeypatch):
    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    response = news_client.get("/api/v1/news")
    assert response.status_code == 503
    news_provider.assert_not_awaited()
