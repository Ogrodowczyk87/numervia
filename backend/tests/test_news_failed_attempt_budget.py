import httpx
import pytest


@pytest.mark.parametrize(
    "provider,key",
    [("marketaux", "MARKETAUX_API_TOKEN"), ("currents", "CURRENTS_API_KEY")],
)
def test_news_failed_attempt_budget(
    news_client, news_provider, monkeypatch, provider, key
):
    from app.news import cache

    monkeypatch.delenv("MARKETAUX_API_TOKEN", raising=False)
    monkeypatch.setenv(key, "test-token")
    news_provider.side_effect = httpx.ConnectError("private-token")
    assert news_client.get("/api/v1/news").status_code == 502
    assert len(cache.providers[provider].attempts) == 1
    assert news_client.get("/api/v1/news").status_code == 502
    assert len(cache.providers[provider].attempts) == 1
    news_provider.assert_awaited_once()
