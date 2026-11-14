from app.news import DEFAULT_PATH, get_store


def test_news_defaults_to_demo_path(monkeypatch):
    monkeypatch.setenv("NEWS_STATE_PATH", " ")
    assert get_store().path == DEFAULT_PATH
