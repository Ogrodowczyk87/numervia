def test_news_empty(news_client, news_provider, provider_response):
    news_provider.return_value = provider_response({"data": []})
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json() == []
