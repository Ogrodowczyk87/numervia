def test_news_unknown_feed(news_client, news_provider):
    assert news_client.get("/api/v1/news?feed=arbitrary-query").status_code == 422
    assert news_client.post("/api/v1/news/refresh").status_code == 404
    news_provider.assert_not_awaited()
