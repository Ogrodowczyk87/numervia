def test_currents_env_fallback(
    news_client, news_provider, provider_response, monkeypatch, tmp_path
):
    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", " ")
    path = tmp_path / ".env"
    path.write_text("CURRENTS_API_KEY=file-currents-token\n")
    monkeypatch.setattr("app.news.ENV_PATH", path)
    news_provider.return_value = provider_response({"status": "ok", "news": []})
    assert news_client.get("/api/v1/news").json() == []
    assert news_provider.call_args.kwargs["headers"] == {
        "Authorization": "Bearer file-currents-token"
    }
