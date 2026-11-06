import pytest


@pytest.mark.parametrize(
    "payload", [{}, {"data": None}, {"data": [{}]}, {"data": [{"title": "Incomplete"}]}]
)
def test_news_invalid_payload(news_client, news_provider, provider_response, payload):
    news_provider.return_value = provider_response(payload)
    assert news_client.get("/api/v1/news").status_code == 502
