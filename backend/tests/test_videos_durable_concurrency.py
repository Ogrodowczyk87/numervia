import asyncio
from concurrent.futures import ProcessPoolExecutor

from app.video_refresh import refresh_category
from app.video_store import FileVideoStore


def _refresh(arguments):
    path, now = arguments

    async def fetch(category):
        return []

    return asyncio.run(
        refresh_category(FileVideoStore(path), "Finance", now, now, fetch)
    ).status


def test_video_concurrent_processes_share_one_reservation(saved_videos):
    store, now, _ = saved_videos
    with ProcessPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(_refresh, [(store.path, now), (store.path, now)]))
    assert sorted(results) == ["skipped", "updated"]
    assert len(store.read().attempts) == 1
