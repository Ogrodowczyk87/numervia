from unittest.mock import Mock

import pytest

from app.content.stores import select_news_store, select_video_store
from app.news.s3_store import S3NewsStore
from app.news.store import FileNewsStore
from app.videos.s3_store import S3VideoStore
from app.videos.store import FileVideoStore


@pytest.mark.parametrize(
    ("select_store", "local_class", "s3_class", "expected_key"),
    [
        (
            select_news_store,
            FileNewsStore,
            S3NewsStore,
            "news/state.json",
        ),
        (
            select_video_store,
            FileVideoStore,
            S3VideoStore,
            "videos/state.json",
        ),
    ],
)
def test_select_s3_store(
    monkeypatch,
    tmp_path,
    select_store,
    local_class,
    s3_class,
    expected_key,
):
    monkeypatch.setenv("CONTENT_STATE_BACKEND", "s3")
    monkeypatch.setenv("CONTENT_STATE_BUCKET", "example-state")
    monkeypatch.setenv("NEWS_STATE_KEY", "news/state.json")
    monkeypatch.setenv("VIDEOS_STATE_KEY", "videos/state.json")

    client = object()
    create_client = Mock(return_value=client)
    monkeypatch.setattr(
        "app.content.stores.get_s3_client",
        create_client,
    )

    local_store = local_class(tmp_path / "state.json")

    result = select_store(local_store)

    assert isinstance(result, s3_class)
    assert result.client is client
    assert result.bucket == "example-state"
    assert result.key == expected_key
    create_client.assert_called_once_with()
