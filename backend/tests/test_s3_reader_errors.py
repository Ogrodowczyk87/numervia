from unittest.mock import Mock

import pytest
from botocore.exceptions import ClientError

from app.s3_reader import S3StateUnavailable, read_s3_object


@pytest.mark.parametrize("error_code", ["NoSuchKey", "AccessDenied"])
def test_converts_s3_errors_to_state_unavailable(error_code):
    client = Mock()
    original_error = ClientError(
        {
            "Error": {
                "Code": error_code,
                "Message": "Simulated S3 error",
            }
        },
        "GetObject",
    )
    client.get_object.side_effect = original_error

    with pytest.raises(S3StateUnavailable) as caught:
        read_s3_object(client, "test-bucket", "news/state.json")

    assert caught.value.__cause__ is original_error
    client.get_object.assert_called_once_with(
        Bucket="test-bucket",
        Key="news/state.json",
    )
