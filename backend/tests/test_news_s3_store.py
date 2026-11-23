import json
from io import BytesIO
from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from app.news_s3_store import S3NewsStore
from app.news_state import NewsState
from app.news_store import StateUnavailable


@pytest.mark.parametrize(
    "scenario",
    ["valid", "invalid_json", "missing_fields", "s3_error"],
)
def test_reads_and_validates_news_state(scenario):
    expected = NewsState(mode="live")
    payload = expected.model_dump_json().encode()

    if scenario == "invalid_json":
        payload = b"not valid JSON"
    elif scenario == "missing_fields":
        data = json.loads(payload)
        del data["providers"]["marketaux"]["attempts"]
        payload = json.dumps(data).encode()

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

    store = S3NewsStore(client, "test-bucket", "news/state.json")

    if scenario == "valid":
        assert store.read() == expected
    else:
        with pytest.raises(StateUnavailable) as caught:
            store.read()
        assert caught.value.__cause__ is not None

    if scenario != "s3_error":
        assert body.closed

    client.get_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="news/state.json",
    )
