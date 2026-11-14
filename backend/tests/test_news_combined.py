import pytest

from app.news_providers import NewsArticle


@pytest.mark.parametrize("duplicate", [False, True])
def test_news_combined(news_client, saved_news, news_article, duplicate):
    save = saved_news[2]
    save(articles=[NewsArticle(**news_article)])
    other = NewsArticle(
        **{
            **news_article,
            "provider": "currents",
            "url": news_article["url"] + ("#story" if duplicate else "/other"),
        }
    )
    save("currents:overview", [other])
    response = news_client.get("/api/v1/news").json()
    assert len(response["articles"]) == (1 if duplicate else 2)
