def test_news_api_does_not_expose_private_state(news_client, saved_news):
    store, _, save = saved_news
    save()

    def configure(state):
        state.mode = "live"
        state.providers["marketaux"].last_error_code = "credentials"
        state.providers["marketaux"].provider_disabled = True

    store.update(configure)
    response = news_client.get("/api/v1/news")
    assert response.json()["demo"] is False
    assert set(response.json()) == {
        "articles",
        "feed",
        "fetched_at",
        "fresh_until",
        "serve_until",
        "stale",
        "demo",
    }
    assert "credentials" not in response.text
