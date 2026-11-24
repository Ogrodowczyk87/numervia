import pytest

from app.news.providers import NewsArticle


@pytest.mark.parametrize("failed", ["marketaux", "currents"])
@pytest.mark.parametrize("age", [0, 7, 24])
def test_news_partial_failure(news_client, saved_news, news_article, failed, age):
    store, _, save = saved_news
    healthy = "currents" if failed == "marketaux" else "marketaux"
    save(f"{healthy}:overview", [NewsArticle(**{**news_article, "provider": healthy})])
    save(
        f"{failed}:overview",
        [
            NewsArticle(
                **{**news_article, "provider": failed, "url": "https://example.com/old"}
            )
        ],
        age_hours=age,
    )
    store.update(
        lambda state: setattr(state.providers[failed], "provider_disabled", True)
    )
    result = news_client.get("/api/v1/news").json()
    assert len(result["articles"]) == (1 if age == 24 else 2)
    assert result["stale"] is (age == 7)
