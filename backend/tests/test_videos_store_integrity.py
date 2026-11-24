import json

import pytest

from app.videos.state import VideoState
from app.videos.store import FileVideoStore, VideoStateUnavailable


@pytest.mark.parametrize(
    "failure", ["reset", "missing_budget_record", "schema", "oversize", "replace"]
)
def test_video_store_rejects_reset_and_corrupt_state(
    saved_videos, monkeypatch, failure
):
    store = saved_videos[0]
    original = store.path.read_bytes()
    if failure == "reset":
        with pytest.raises(FileExistsError):
            store.initialize(VideoState(mode="demo"))
        assert store.path.read_bytes() == original
    elif failure == "replace":

        def fail(*args):
            raise OSError("failure")

        monkeypatch.setattr("app.videos.store.os.replace", fail)
        with pytest.raises(VideoStateUnavailable):
            store.update(lambda state: None)
        assert store.path.read_bytes() == original
        assert len(list(store.path.parent.iterdir())) == 2
    else:
        data = json.loads(original)
        if failure == "missing_budget_record":
            del data["attempts"]
        elif failure == "schema":
            data["schema_version"] = 99
        store.path.write_text(
            " " * (1024 * 1024 + 1) if failure == "oversize" else json.dumps(data)
        )
        with pytest.raises(VideoStateUnavailable):
            FileVideoStore(store.path).read()
