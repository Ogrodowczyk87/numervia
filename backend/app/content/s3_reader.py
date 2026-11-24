"""Read saved state from S3 without modifying it."""

from contextlib import closing
from typing import Any

from botocore.exceptions import BotoCoreError, ClientError

MAX_STATE_BYTES = 1024 * 1024


class S3StateUnavailable(RuntimeError):
    pass


def read_s3_object(
    client: Any,
    bucket: str,
    key: str,
) -> bytes:
    try:
        response = client.get_object(
            Bucket=bucket,
            Key=key,
        )

        with closing(response["Body"]) as body:
            if response["ContentLength"] > MAX_STATE_BYTES:
                raise ValueError("State exceeds size limit")

            payload = body.read(MAX_STATE_BYTES + 1)

        if len(payload) > MAX_STATE_BYTES:
            raise ValueError("State exceeds size limit")

        return payload

    except (BotoCoreError, ClientError, OSError, ValueError) as error:
        raise S3StateUnavailable(
            "Saved state could not be read from S3"
        ) from error