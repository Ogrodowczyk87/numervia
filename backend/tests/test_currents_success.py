import pytest


@pytest.mark.parametrize(
    "image", [None, "", "None", "null", "https://example.com/a.jpg"]
)
def test_currents_success(
    news_client, news_provider, currents_article, provider_response, monkeypatch, image
):
    monkeypatch.delenv("MARKETAUX_API_TOKEN")
    monkeypatch.setenv("CURRENTS_API_KEY", "currents-test-token")
    currents_article["image"] = image
    news_provider.return_value = provider_response(
        {"status": "ok", "news": [currents_article]}
    )
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json() == [
        {
            "title": currents_article["title"],
            "url": currents_article["url"],
            "source": "publisher.example",
            "published_at": "2026-11-08T10:00:00+00:00",
            "image_url": image if image == "https://example.com/a.jpg" else None,
            "provider": "currents",
        }
    ]
    assert "currents-test-token" not in response.text
    news_provider.assert_awaited_once_with(
        "https://api.currentsapi.services/v2/latest-news",
        headers={"Authorization": "Bearer currents-test-token"},
        params={
            "language": "en",
            "category": "economy_business_finance",
            "page_size": 20,
        },
    )
