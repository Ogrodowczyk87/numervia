from app.news_providers import NewsArticle


def test_news_success(news_client, saved_news, news_article, news_provider):
    _, _, save = saved_news
    save(articles=[NewsArticle(**news_article)])
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json()["articles"] == [news_article]
    assert response.json()["demo"] is True
    assert response.headers["Cache-Control"] == "no-store"
    assert "providers" not in response.json()
    news_provider.assert_not_awaited()
