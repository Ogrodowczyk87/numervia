from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.news.routes import current_time, get_store, router
from app.news.store import FileNewsStore


def test_recreated_api_reads_same_state_without_provider_requests(
    saved_news, news_provider
):
    store, now, save = saved_news
    save()
    before = store.path.read_bytes()
    for _ in range(2):
        restarted = FastAPI()
        restarted.include_router(router)
        restarted.dependency_overrides[get_store] = lambda: FileNewsStore(store.path)
        restarted.dependency_overrides[current_time] = lambda: now
        with TestClient(restarted) as client:
            assert client.get("/api/v1/news").status_code == 200
    assert store.path.read_bytes() == before
    news_provider.assert_not_awaited()
