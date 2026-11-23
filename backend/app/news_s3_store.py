"""Read and validate saved news state from S3."""

from typing import Any

from app.news_state import NewsState
from app.news_store import StateUnavailable
from app.s3_reader import S3StateUnavailable, read_s3_object


class S3NewsStore:
    def __init__(self, client: Any, bucket: str, key: str):
        self.client = client
        self.bucket = bucket
        self.key = key

    def read(self) -> NewsState:
        try:
            payload = read_s3_object(
                self.client,
                self.bucket,
                self.key,
            )

            state = NewsState.model_validate_json(payload)

            records = [
                state,
                *state.providers.values(),
                *state.feeds.values(),
            ]

            if any(
                record.model_fields_set != set(type(record).model_fields)
                for record in records
            ):
                raise ValueError("Persisted state has missing fields")

            return state

        except (S3StateUnavailable, ValueError) as error:
            raise StateUnavailable(
                "News state is missing, invalid or unreadable"
            ) from error