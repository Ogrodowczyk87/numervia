from concurrent.futures import ThreadPoolExecutor


def test_news_concurrent_requests(news_client, saved_news, news_provider):
    saved_news[2]()
    with ThreadPoolExecutor(max_workers=4) as pool:
        statuses = list(
            pool.map(lambda _: news_client.get("/api/v1/news").status_code, range(20))
        )
    assert statuses == [200] * 20
    news_provider.assert_not_awaited()
