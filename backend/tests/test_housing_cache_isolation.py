from app.news_providers import NewsArticle


def test_housing_cache_isolation(news_client, saved_news, news_article):
    save = saved_news[2]
    save(articles=[NewsArticle(**news_article)])
    save(
        "currents:housing",
        [
            NewsArticle(
                **{
                    **news_article,
                    "provider": "currents",
                    "title": "Mortgage rates",
                    "url": "https://example.com/housing",
                }
            )
        ],
    )
    assert (
        news_client.get("/api/v1/news").json()["articles"][0]["title"]
        == news_article["title"]
    )
    assert (
        news_client.get("/api/v1/news?feed=housing").json()["articles"][0]["title"]
        == "Mortgage rates"
    )
