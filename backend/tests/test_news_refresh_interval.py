import pytest


@pytest.mark.parametrize(
    "provider,key",
    [("marketaux", "MARKETAUX_API_TOKEN"), ("currents", "CURRENTS_API_KEY")],
)
@pytest.mark.parametrize("status", [200, 500])
def test_news_refresh_interval(
    news_client, news_provider, provider_response, monkeypatch, provider, key, status
):
    monkeypatch.delenv("MARKETAUX_API_TOKEN", raising=False)
    monkeypatch.setenv(key, "test-token")
    now = [100.0]
    monkeypatch.setattr("app.news.time.monotonic", lambda: now[0])
    payload = {"data": []} if provider == "marketaux" else {"status": "ok", "news": []}
    news_provider.return_value = provider_response(payload, status)
    expected = 200 if status == 200 else 502
    assert news_client.get("/api/v1/news").status_code == expected
    for elapsed in (3600, 5 * 3600, 6 * 3600 - 1):
        now[0] = 100.0 + elapsed
        assert news_client.get("/api/v1/news").status_code == expected
        assert news_provider.await_count == 1
    now[0] = 100.0 + 6 * 3600
    news_provider.return_value = provider_response(payload)
    assert news_client.get("/api/v1/news").status_code == 200
    assert news_provider.await_count == 2
