def test_news_success(news_client, news_provider, news_article, provider_response):
    news_provider.return_value = provider_response({"data": [news_article]})
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json() == [news_article]
    assert "test-token" not in response.text
    news_provider.assert_awaited_once_with(
        "https://api.marketaux.com/v1/news/all",
        params={"api_token": "test-token", "language": "en", "limit": 3},
    )
