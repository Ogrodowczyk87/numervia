import pytest


@pytest.mark.parametrize("duplicate", [False, True])
def test_news_combined(
    news_client,
    news_provider,
    news_article,
    currents_article,
    provider_response,
    monkeypatch,
    duplicate,
):
    monkeypatch.setenv("CURRENTS_API_KEY", "currents-test-token")
    if duplicate:
        currents_article["url"] = news_article["url"] + "#story"
    news_provider.side_effect = [
        provider_response({"data": [news_article]}),
        provider_response({"status": "ok", "news": [currents_article]}),
    ]
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert len(response.json()) == (1 if duplicate else 2)
    assert response.json()[0] == news_article
    if not duplicate:
        assert response.json()[1]["provider"] == "currents"
    assert news_provider.await_count == 2
    assert news_client.get("/api/v1/news").json() == response.json()
    assert news_provider.await_count == 2
