import pytest

from app.news_state import NewsState
from app.news_store import MAX_STATE_BYTES, FileNewsStore, StateUnavailable


@pytest.mark.parametrize(
    "case",
    ["reinitialize", "unknown_schema", "oversize", "replace_failure", "missing_budget"],
)
def test_store_rejects_reset_corruption_and_preserves_old_file(
    tmp_path, monkeypatch, case
):
    store = FileNewsStore(tmp_path / "state.json")
    store.initialize(NewsState(mode="demo"))
    original = store.path.read_bytes()
    if case == "reinitialize":
        with pytest.raises(FileExistsError):
            store.initialize(NewsState(mode="live"))
        assert store.path.read_bytes() == original
    elif case == "missing_budget":
        import json

        data = json.loads(original)
        del data["providers"]["marketaux"]["attempts"]
        store.path.write_text(json.dumps(data))
        with pytest.raises(StateUnavailable):
            store.read()
    elif case in ("unknown_schema", "oversize"):
        store.path.write_bytes(
            original.replace(b'"schema_version":1', b'"schema_version":2')
            if case == "unknown_schema"
            else b" " * (MAX_STATE_BYTES + 1)
        )
        with pytest.raises(StateUnavailable):
            store.read()
    else:

        def fail(*args):
            raise OSError("replace failed")

        monkeypatch.setattr("app.news_store.os.replace", fail)
        with pytest.raises(StateUnavailable):
            store.update(lambda state: None)
        assert store.path.read_bytes() == original
        assert sorted(p.name for p in tmp_path.iterdir()) == [
            "state.json",
            "state.json.lock",
        ]
