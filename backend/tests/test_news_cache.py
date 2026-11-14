def test_news_cache(news_client, saved_news, news_provider):
    store, _, save = saved_news
    save()
    before = store.path.read_bytes()
    for _ in range(1000):
        assert news_client.get("/api/v1/news").status_code == 200
    assert store.path.read_bytes() == before
    news_provider.assert_not_awaited()
