def test_news_empty(news_client, saved_news):
    saved_news[2]()
    response = news_client.get("/api/v1/news")
    assert response.status_code == 200
    assert response.json()["articles"] == []
