from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def news_provider(monkeypatch, tmp_path):
    monkeypatch.setenv("MARKETAUX_API_TOKEN", "test-token")
    monkeypatch.setattr("app.news.ENV_PATH", tmp_path / "missing.env")
    mock = AsyncMock()
    monkeypatch.setattr("app.news.httpx.AsyncClient.get", mock)
    return mock


@pytest.fixture
def news_client(news_provider):
    with TestClient(app) as client:
        yield client


@pytest.fixture
def news_article():
    return {
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
