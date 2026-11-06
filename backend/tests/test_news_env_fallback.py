def test_news_env_fallback(
    news_client, news_provider, provider_response, monkeypatch, tmp_path
):
    path = tmp_path / ".env"
    path.write_text("MARKETAUX_API_TOKEN=file-token\n")
    monkeypatch.setattr("app.news.ENV_PATH", path)
    monkeypatch.setenv("MARKETAUX_API_TOKEN", " ")
    news_provider.return_value = provider_response({"data": []})
    assert news_client.get("/api/v1/news").status_code == 200
    assert news_provider.call_args.kwargs["params"]["api_token"] == "file-token"
