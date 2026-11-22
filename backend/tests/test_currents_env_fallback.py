import pytest

from app.news import DEFAULT_PATH, get_store


@pytest.mark.parametrize("preview_enabled", [False, True])
def test_news_selects_local_default_without_external_state(monkeypatch, tmp_path, preview_enabled):
    monkeypatch.setenv("NEWS_STATE_PATH", " ")
    marker = tmp_path / "news-preview.enabled"
    live_path = tmp_path / "news-live.json"
    monkeypatch.setattr("app.news.PREVIEW_MARKER", marker)
    monkeypatch.setattr("app.news.LIVE_PATH", live_path)
    if preview_enabled:
        marker.write_text("enabled")
    assert get_store().path == (live_path if preview_enabled else DEFAULT_PATH)
