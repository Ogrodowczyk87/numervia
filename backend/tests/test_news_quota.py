import pytest


@pytest.mark.parametrize("status", [402, 429])
def test_news_quota(news_client, news_provider, provider_response, monkeypatch, status):
    now = [100.0]
    monkeypatch.setattr("app.news.time.monotonic", lambda: now[0])
    news_provider.return_value = provider_response({"error": "test-token"}, status)
    first = news_client.get("/api/v1/news")
    assert first.status_code == 429
    assert first.headers["Retry-After"] == "21600"
    assert "request limit reached" in first.json()["detail"]
    assert "test-token" not in first.text
    assert news_client.get("/api/v1/news").status_code == 429
    assert news_provider.await_count == 1
    now[0] += 21601
    news_provider.return_value = provider_response({"data": []})
    assert news_client.get("/api/v1/news").status_code == 200
    assert news_provider.await_count == 2
