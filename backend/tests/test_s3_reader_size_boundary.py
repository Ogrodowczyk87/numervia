from io import BytesIO
from unittest.mock import Mock

from app.s3_reader import read_s3_object


def test_accepts_exactly_one_mib_and_closes_body():
    payload = b"x" * (1024 * 1024)
    body = BytesIO(payload)
    client = Mock()
    client.get_object.return_value = {
        "Body": body,
        "ContentLength": len(payload),
    }

    result = read_s3_object(client, "test-bucket", "news/state.json")

    assert result == payload
    assert body.closed
