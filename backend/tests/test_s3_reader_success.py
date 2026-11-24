from io import BytesIO
from unittest.mock import Mock

from app.content.s3_reader import read_s3_object


def test_reads_s3_object_and_closes_body():
    payload = b'{"status":"ok"}'
    body = BytesIO(payload)
    client = Mock()
    client.get_object.return_value = {
        "Body": body,
        "ContentLength": len(payload),
    }

    result = read_s3_object(
        client,
        "test-bucket",
        "news/state.json",
    )

    assert result == payload
    assert body.closed
    client.get_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="news/state.json",
    )
