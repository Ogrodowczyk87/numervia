import os
from typing import Literal


class ContentConfigurationError(ValueError):
    pass


def get_content_backend() -> Literal["local", "s3"]:
    value = os.getenv("CONTENT_STATE_BACKEND", "local").strip()

    if value == "local":
        return "local"

    if value == "s3":
        return "s3"

    raise ContentConfigurationError(
        "CONTENT_STATE_BACKEND must be 'local' or 's3'"
    )

def get_s3_settings() -> tuple[str, str, str]:
    names = (
        "CONTENT_STATE_BUCKET",
        "NEWS_STATE_KEY",
        "VIDEOS_STATE_KEY",
    )
    values = tuple(os.getenv(name, "").strip() for name in names)

    missing = [
        name
        for name, value in zip(names, values)
        if not value
    ]

    if missing:
        raise ContentConfigurationError(
            "Missing S3 settings: " + ", ".join(missing)
        )

    return values[0], values[1], values[2]