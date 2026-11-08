def test_news_unknown_feed(news_client, news_provider):
    assert news_client.get("/api/v1/news?feed=arbitrary-query").status_code == 422
    news_provider.assert_not_awaited()
