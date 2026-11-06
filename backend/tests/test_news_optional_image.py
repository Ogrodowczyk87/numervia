import pytest


@pytest.mark.parametrize("image", [None, "", "missing"])
def test_news_optional_image(
    news_client, news_provider, news_article, provider_response, image
):
    if image == "missing":
        news_article.pop("image_url")
    else:
        news_article["image_url"] = image
    news_provider.return_value = provider_response({"data": [news_article]})
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json()[0]["image_url"] is None
