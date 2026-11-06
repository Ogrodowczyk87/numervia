import pytest


@pytest.mark.parametrize("status", [401, 403, 429, 500])
def test_news_provider_status(news_client, news_provider, provider_response, status):
    news_provider.return_value = provider_response({"error": "test-token"}, status)
    response = news_client.get("/api/v1/news")
    assert response.status_code == 502
    assert response.json() == {"detail": "News is temporarily unavailable."}
    assert "test-token" not in response.text
