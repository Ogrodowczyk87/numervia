"""Read and validate saved video state from S3."""

from typing import Any

from app.s3_reader import S3StateUnavailable, read_s3_object
from app.video_state import VideoState
from app.video_store import VideoStateUnavailable


class S3VideoStore:
    def __init__(self, client: Any, bucket: str, key: str):
        self.client = client
        self.bucket = bucket
        self.key = key

    def read(self) -> VideoState:
        try:
            payload = read_s3_object(
                self.client,
                self.bucket,
                self.key,
            )

            state = VideoState.model_validate_json(payload)

            records = [state, *state.categories.values()]
            if state.budget is not None:
                records.append(state.budget)

            if any(
                record.model_fields_set != set(type(record).model_fields)
                for record in records
            ):
                raise ValueError("Persisted state has missing fields")

            return state

        except (S3StateUnavailable, ValueError) as error:
            raise VideoStateUnavailable(
                "Video state is missing, invalid or unreadable"
            ) from error