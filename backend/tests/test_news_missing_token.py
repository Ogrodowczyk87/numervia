def test_saved_news_does_not_require_provider_tokens(
    news_client, saved_news, monkeypatch, news_provider
):
    for key in ("MARKETAUX_API_TOKEN", "CURRENTS_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    saved_news[2]()
    assert news_client.get("/api/v1/news").status_code == 200
    news_provider.assert_not_awaited()
