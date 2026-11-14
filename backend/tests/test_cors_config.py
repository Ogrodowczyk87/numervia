import pytest

from app.main import create_app


@pytest.mark.parametrize(
    "origin",
    [
        "*",
        "https://example.com/",
        "https://user:pass@example.com",
        "http://example.com",
        "https://example.com?token=secret",
    ],
)
def test_cors_rejects_unsafe_or_mistyped_origin(monkeypatch, origin):
    monkeypatch.setenv("ALLOWED_ORIGINS", origin)
    with pytest.raises(ValueError):
        create_app()
