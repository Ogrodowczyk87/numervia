import pytest


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"status": "error", "news": []},
        {"status": "ok", "news": {}},
        {"status": "ok", "news": [None]},
        {"status": "ok", "news": [{"title": "Incomplete"}]},
    ],
)
def test_currents_invalid_payload(
    news_client, news_provider, provider_response, monkeypatch, payload
):
    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", "currents-test-token")
    news_provider.return_value = provider_response(payload)
    assert news_client.get("/api/v1/news").status_code == 502
    assert news_client.get("/api/v1/news").status_code == 502
    news_provider.assert_awaited_once()
