import json
from datetime import UTC, datetime
from io import BytesIO
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from app.videos.s3_store import S3VideoStore
from app.videos.state import SavedCategory, VideoBudget, VideoState
from app.videos.store import VideoStateUnavailable


@pytest.mark.parametrize(
    "scenario",
    [
        "valid",
        "invalid_json",
        "missing_attempts",
        "missing_budget_field",
        "missing_category_field",
        "s3_error",
    ],
)
def test_reads_and_validates_video_state(scenario):
    expected = VideoState(
        mode="live",
        budget=VideoBudget(
            daily_quota=100,
            cost_per_search=1,
            request_budget=80,
        ),
        quota_confirmed_at=datetime(2026, 11, 23, tzinfo=UTC),
        categories={"Finance": SavedCategory()},
    )
    data = expected.model_dump(mode="json")

    if scenario == "missing_attempts":
        del data["attempts"]
    elif scenario == "missing_budget_field":
        del data["budget"]["request_budget"]
    elif scenario == "missing_category_field":
        del data["categories"]["Finance"]["reservation_id"]

    payload = (
        b"not valid JSON"
        if scenario == "invalid_json"
        else json.dumps(data).encode()
    )
    body = BytesIO(payload)
    client = Mock()

    if scenario == "s3_error":
        client.get_object.side_effect = ClientError(
            {"Error": {"Code": "NoSuchKey", "Message": "Missing"}},
            "GetObject",
        )
    else:
        client.get_object.return_value = {
            "Body": body,
            "ContentLength": len(payload),
        }

    store = S3VideoStore(client, "test-bucket", "videos/state.json")

    if scenario == "valid":
        assert store.read() == expected
    else:
        with pytest.raises(VideoStateUnavailable) as caught:
            store.read()
        assert caught.value.__cause__ is not None

    if scenario != "s3_error":
        assert body.closed

    client.get_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="videos/state.json",
    )
