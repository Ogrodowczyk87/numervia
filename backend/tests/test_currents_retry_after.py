import pytest


@pytest.mark.parametrize("delay,expected", [(7200, 21600), (43200, 43200)])
def test_currents_retry_after(news_client, news_provider, monkeypatch, delay, expected):
    import httpx

    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", "currents-test-token")
    news_provider.return_value = httpx.Response(
        429,
        headers={"Retry-After": str(delay)},
        request=httpx.Request("GET", "https://example.com"),
    )
    response = news_client.get("/api/v1/news")
    assert response.status_code == 429
    assert int(response.headers["Retry-After"]) >= expected - 1
    assert news_client.get("/api/v1/news").status_code == 429
    news_provider.assert_awaited_once()
