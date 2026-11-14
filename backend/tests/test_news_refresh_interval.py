import pytest


@pytest.mark.parametrize("age,stale", [(0, False), (6, False), (7, True), (23, True)])
def test_news_actual_freshness_is_recomputed(news_client, saved_news, age, stale):
    saved_news[2](age_hours=age)
    assert news_client.get("/api/v1/news").json()["stale"] is stale
