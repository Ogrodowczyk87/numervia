from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.video_store import FileVideoStore
from app.videos import current_time, get_store, router


def test_recreated_video_api_keeps_saved_state_and_private_budget(
    saved_videos, video_provider
):
    store, now, save = saved_videos
    save()
    before = store.path.read_bytes()
    for _ in range(2):
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_store] = lambda: FileVideoStore(store.path)
        app.dependency_overrides[current_time] = lambda: now
        with TestClient(app) as client:
            result = client.get("/api/v1/videos").json()
            assert set(result) == {
                "videos",
                "updated_at",
                "fresh_until",
                "serve_until",
                "stale",
                "demo",
            }
    assert store.path.read_bytes() == before
    video_provider.assert_not_awaited()
