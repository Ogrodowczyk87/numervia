def test_currents_retry_after(news_client, news_provider, monkeypatch):
    import httpx

    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", "currents-test-token")
    news_provider.return_value = httpx.Response(
        429,
        headers={"Retry-After": "7200"},
        request=httpx.Request("GET", "https://example.com"),
    )
    response = news_client.get("/api/v1/news")
    assert response.status_code == 429
    assert int(response.headers["Retry-After"]) >= 7199
    assert news_client.get("/api/v1/news").status_code == 429
    news_provider.assert_awaited_once()
