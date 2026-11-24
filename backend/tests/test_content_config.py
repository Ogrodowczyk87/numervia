import pytest

from app.content.config import (
    ContentConfigurationError,
    get_content_backend,
)


@pytest.mark.parametrize(
    ("configured", "expected"),
    [
        (None, "local"),
        ("local", "local"),
        ("s3", "s3"),
        (" s3 ", "s3"),
        ("", None),
        ("s33", None),
    ],
)
def test_content_backend_configuration(monkeypatch, configured, expected):
    if configured is None:
        monkeypatch.delenv("CONTENT_STATE_BACKEND", raising=False)
    else:
        monkeypatch.setenv("CONTENT_STATE_BACKEND", configured)

    if expected is None:
        with pytest.raises(ContentConfigurationError):
            get_content_backend()
    else:
        assert get_content_backend() == expected
