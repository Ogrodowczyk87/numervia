from app.news import get_store


def test_news_state_path_comes_from_environment(monkeypatch, tmp_path):
    path = tmp_path / "selected.json"
    monkeypatch.setenv("NEWS_STATE_PATH", str(path))
    assert get_store().path == path
