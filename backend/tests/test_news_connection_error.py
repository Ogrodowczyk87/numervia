import httpx
import pytest


@pytest.mark.parametrize(
    "error", [httpx.ConnectError("test-token"), httpx.ReadTimeout("test-token")]
)
def test_news_connection_error(news_client, news_provider, error):
    news_provider.side_effect = error
    response = news_client.get("/api/v1/news")
    assert response.status_code == 502
    assert "test-token" not in response.text
