from io import BytesIO
from unittest.mock import Mock

import pytest

from app.content.s3_reader import S3StateUnavailable, read_s3_object


def test_rejects_oversized_body_despite_smaller_declared_size():
    body = BytesIO(b"x" * (2 * 1024 * 1024))
    read = Mock(wraps=body.read)
    body.read = read
    client = Mock()
    client.get_object.return_value = {
        "Body": body,
        "ContentLength": 1024,
    }

    with pytest.raises(S3StateUnavailable) as caught:
        read_s3_object(client, "test-bucket", "news/state.json")

    read.assert_called_once_with(1024 * 1024 + 1)
    assert body.closed
    assert isinstance(caught.value.__cause__, ValueError)
