from unittest.mock import Mock

import pytest

from app.content.s3_reader import S3StateUnavailable, read_s3_object


def test_closes_stream_and_rejects_failed_read():
    original_error = OSError("Connection interrupted during read")
    body = Mock()
    body.read.side_effect = original_error
    client = Mock()
    client.get_object.return_value = {
        "Body": body,
        "ContentLength": 128,
    }

    with pytest.raises(S3StateUnavailable) as caught:
        read_s3_object(client, "test-bucket", "news/state.json")

    assert caught.value.__cause__ is original_error
    body.read.assert_called_once_with(1024 * 1024 + 1)
    body.close.assert_called_once_with()
