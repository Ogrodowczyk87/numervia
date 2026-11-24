import pytest

from app.content.config import ContentConfigurationError, get_s3_settings


@pytest.mark.parametrize(
    ("overrides", "expected", "missing"),
    [
        ({}, ("example-state", "news/state.json", "videos/state.json"), []),
        (
            {
                "CONTENT_STATE_BUCKET": " example-state ",
                "NEWS_STATE_KEY": " news/state.json ",
                "VIDEOS_STATE_KEY": " videos/state.json ",
            },
            ("example-state", "news/state.json", "videos/state.json"),
            [],
        ),
        ({"CONTENT_STATE_BUCKET": None}, None, ["CONTENT_STATE_BUCKET"]),
        ({"NEWS_STATE_KEY": None}, None, ["NEWS_STATE_KEY"]),
        ({"VIDEOS_STATE_KEY": None}, None, ["VIDEOS_STATE_KEY"]),
        ({"NEWS_STATE_KEY": ""}, None, ["NEWS_STATE_KEY"]),
        ({"VIDEOS_STATE_KEY": "   "}, None, ["VIDEOS_STATE_KEY"]),
        (
            {
                "CONTENT_STATE_BUCKET": None,
                "NEWS_STATE_KEY": None,
                "VIDEOS_STATE_KEY": None,
            },
            None,
            ["CONTENT_STATE_BUCKET", "NEWS_STATE_KEY", "VIDEOS_STATE_KEY"],
        ),
    ],
)
def test_s3_settings_configuration(monkeypatch, overrides, expected, missing):
    settings = {
        "CONTENT_STATE_BUCKET": "example-state",
        "NEWS_STATE_KEY": "news/state.json",
        "VIDEOS_STATE_KEY": "videos/state.json",
    }
    settings.update(overrides)

    for name, value in settings.items():
        if value is None:
            monkeypatch.delenv(name, raising=False)
        else:
            monkeypatch.setenv(name, value)

    if missing:
        with pytest.raises(ContentConfigurationError) as error:
            get_s3_settings()

        assert str(error.value) == "Missing S3 settings: " + ", ".join(missing)
    else:
        assert get_s3_settings() == expected
