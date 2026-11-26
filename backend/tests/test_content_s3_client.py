from unittest.mock import Mock

from app.content.s3_client import get_s3_client


def test_s3_client_configuration_and_reuse(monkeypatch):
    client = object()
    create_client = Mock(return_value=client)
    monkeypatch.setattr("app.content.s3_client.boto3.client", create_client)
    get_s3_client.cache_clear()

    try:
        assert create_client.call_count == 0

        first = get_s3_client()
        second = get_s3_client()

        assert first is client
        assert second is first
        create_client.assert_called_once()

        args, kwargs = create_client.call_args
        assert args == ("s3",)
        assert set(kwargs) == {"config"}

        config = kwargs["config"]
        assert config.connect_timeout == 2
        assert config.read_timeout == 3
        assert config.retries == {
            "mode": "standard",
            "total_max_attempts": 1,
        }
    finally:
        get_s3_client.cache_clear()
