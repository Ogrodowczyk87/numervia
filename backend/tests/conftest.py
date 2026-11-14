from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def news_provider(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("app.news_refresh.httpx.AsyncClient.get", mock)
    return mock


@pytest.fixture
def saved_news(tmp_path):
    from datetime import UTC, datetime, timedelta

    from app.news_state import NewsSnapshot, NewsState, StoredFeed
    from app.news_store import FileNewsStore

    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    store = FileNewsStore(tmp_path / "news.json")
    store.initialize(NewsState(mode="demo"))

    def save(key="marketaux:overview", articles=None, age_hours=0):
        def change(state):
            fetched = now - timedelta(hours=age_hours)
            state.feeds[key] = StoredFeed(
                snapshot=NewsSnapshot(
                    articles=articles or [],
                    fetched_at=fetched,
                    fresh_until=fetched + timedelta(hours=6, minutes=5),
                    serve_until=fetched + timedelta(hours=24),
                )
            )

        store.update(change)

    return store, now, save


@pytest.fixture
def news_client(saved_news, news_provider):
    from app.news import current_time, get_store

    store, now, _ = saved_news
    app.dependency_overrides[get_store] = lambda: store
    app.dependency_overrides[current_time] = lambda: now
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_store, None)
        app.dependency_overrides.pop(current_time, None)


@pytest.fixture
def news_article():
    return {
        "provider": "marketaux",
        "title": "Example financial headline",
        "url": "https://example.com/news",
        "source": "example.com",
        "published_at": "2026-11-06T12:00:00Z",
        "image_url": "https://example.com/image.jpg",
    }


@pytest.fixture
def provider_response():
    def create(payload, status=200):
        return httpx.Response(
            status, json=payload, request=httpx.Request("GET", "https://example.com")
        )

    return create


@pytest.fixture
def video_provider(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr("app.video_refresh.httpx.AsyncClient.get", mock)
    return mock


@pytest.fixture
def saved_videos(tmp_path):
    from datetime import UTC, datetime, timedelta

    from app.video_state import SavedCategory, VideoSnapshot, VideoState
    from app.video_store import FileVideoStore

    now = datetime(2026, 11, 14, 12, tzinfo=UTC)
    store = FileVideoStore(tmp_path / "videos.json")
    store.initialize(VideoState(mode="demo"))

    def save(category="Finance", videos=None, age_hours=0):
        def change(state):
            fetched = now - timedelta(hours=age_hours)
            state.categories[category] = SavedCategory(
                snapshot=VideoSnapshot(
                    videos=videos or [],
                    updated_at=fetched,
                    fresh_until=fetched + timedelta(hours=6, minutes=5),
                    serve_until=fetched + timedelta(hours=24),
                )
            )

        store.update(change)

    return store, now, save


@pytest.fixture
def video_client(saved_videos, video_provider):
    from app.videos import current_time, get_store

    store, now, _ = saved_videos
    app.dependency_overrides[get_store] = lambda: store
    app.dependency_overrides[current_time] = lambda: now
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.pop(get_store, None)
        app.dependency_overrides.pop(current_time, None)


@pytest.fixture
def currents_article():
    return {
        "title": "Example economy headline",
        "url": "https://publisher.example/economy",
        "published": "2026-11-08 10:00:00 +0000",
        "image": "https://publisher.example/image.jpg",
    }
