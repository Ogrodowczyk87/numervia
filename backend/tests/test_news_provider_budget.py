import pytest


@pytest.mark.parametrize(
    "provider,key,limit",
    [("marketaux", "MARKETAUX_API_TOKEN", 80), ("currents", "CURRENTS_API_KEY", 200)],
)
def test_news_provider_budget(
    news_client, news_provider, provider_response, monkeypatch, provider, key, limit
):
    from app.news import cache

    monkeypatch.delenv("MARKETAUX_API_TOKEN", raising=False)
    monkeypatch.setenv(key, "test-token")
    now = [100.0]
    monkeypatch.setattr("app.news.time.monotonic", lambda: now[0])
    state = cache.providers[provider]
    state.attempts.extend([100.0] * limit)
    assert news_client.get("/api/v1/news").status_code == 429
    news_provider.assert_not_awaited()
    now[0] += 86401
    payload = {"data": []} if provider == "marketaux" else {"status": "ok", "news": []}
    news_provider.return_value = provider_response(payload)
    assert news_client.get("/api/v1/news").json() == []
    assert len(state.attempts) == 1
    news_provider.assert_awaited_once()
