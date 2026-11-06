import httpx


def test_news_invalid_json(news_client, news_provider):
    news_provider.return_value = httpx.Response(
        200, text="not json", request=httpx.Request("GET", "https://example.com")
    )
    assert news_client.get("/api/v1/news").status_code == 502
