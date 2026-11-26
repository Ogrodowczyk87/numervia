from unittest.mock import Mock

import pytest

from app.content.stores import select_news_store, select_video_store
from app.news.store import FileNewsStore
from app.videos.store import FileVideoStore


@pytest.mark.parametrize(
    ("select_store", "store_class"),
    [
        (select_news_store, FileNewsStore),
        (select_video_store, FileVideoStore),
    ],
)
def test_local_store_does_not_create_s3_client(
    monkeypatch, tmp_path, select_store, store_class
):
    monkeypatch.setenv("CONTENT_STATE_BACKEND", "local")

    create_client = Mock(
        side_effect=AssertionError("S3 client must not be created")
    )
    monkeypatch.setattr(
        "app.content.stores.get_s3_client",
        create_client,
    )

    local_store = store_class(tmp_path / "state.json")

    result = select_store(local_store)

    assert result is local_store
    create_client.assert_not_called()
