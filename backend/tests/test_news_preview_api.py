def test_preview_api_reads_saved_headlines_without_provider_calls(
    news_client, saved_news, news_provider, monkeypatch, tmp_path
):
    from app.news.demo import demo_articles

    store, now, save = saved_news
    save(articles=demo_articles("marketaux", "overview", now))
    store.update(lambda state: setattr(state, "mode", "live"))
    marker = tmp_path / "preview.enabled"
    marker.write_text("enabled")
    monkeypatch.setattr("app.news.routes.LIVE_PATH", store.path)
    monkeypatch.setattr("app.news.routes.PREVIEW_MARKER", marker)
    before = store.path.read_bytes()

    for _ in range(3):
        response = news_client.get("/api/v1/news")
        assert response.status_code == 200
        body = response.json()
        assert body["preview"] is True
        assert body["demo"] is False
        assert len(body["articles"]) == 3
        assert datetime.fromisoformat(body["fetched_at"]) == now

    news_provider.assert_not_called()
    assert store.path.read_bytes() == before
from datetime import datetime
