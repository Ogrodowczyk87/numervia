import httpx
import pytest


@pytest.mark.parametrize("failed", ["marketaux", "currents"])
@pytest.mark.parametrize("error", [401, 429, 500, "network", "timeout", "invalid"])
def test_news_partial_failure(
    news_client,
    news_provider,
    news_article,
    currents_article,
    provider_response,
    monkeypatch,
    failed,
    error,
):
    monkeypatch.setenv("CURRENTS_API_KEY", "currents-test-token")

    async def request(url, **kwargs):
        provider = "marketaux" if "marketaux" in url else "currents"
        if provider == failed:
            if error == "network":
                raise httpx.ConnectError("private-token")
            if error == "timeout":
                raise TimeoutError("private-token")
            if error == "invalid":
                return provider_response({})
            return provider_response({"error": "private-token"}, error)
        payload = (
            {"data": [news_article]}
            if provider == "marketaux"
            else {"status": "ok", "news": [currents_article]}
        )
        return provider_response(payload)

    news_provider.side_effect = request
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["provider"] != failed
    assert "private-token" not in response.text
    assert news_client.get("/api/v1/news").json() == response.json()
    assert news_provider.await_count == 2
