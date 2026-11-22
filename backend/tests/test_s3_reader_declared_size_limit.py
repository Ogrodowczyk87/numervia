from unittest.mock import Mock

import pytest

from app.s3_reader import S3StateUnavailable, read_s3_object


def test_rejects_declared_size_over_one_mib_without_reading():
    body = Mock()
    client = Mock()
    client.get_object.return_value = {
        "Body": body,
        "ContentLength": 1024 * 1024 + 1,
    }

    with pytest.raises(S3StateUnavailable) as caught:
        read_s3_object(client, "test-bucket", "news/state.json")

    body.read.assert_not_called()
    body.close.assert_called_once_with()
    assert isinstance(caught.value.__cause__, ValueError)
