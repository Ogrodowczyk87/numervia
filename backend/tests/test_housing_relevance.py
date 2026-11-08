def test_housing_relevance(
    news_client, news_provider, currents_article, provider_response, monkeypatch
):
    monkeypatch.setenv("CURRENTS_API_KEY", "test-token")
    entries = [
        {**currents_article, "title": title, "url": f"https://example.com/{index}"}
        for index, title in enumerate(
            [
                "Mortgage rates change",
                "UK house prices rise",
                "Housing supply improves",
                "Commercial property investment",
                "Sports team wins final",
                "Having problems with a partner",
                "Your Daily Mortgage Import Can Leak History Into Evaluation",
            ]
        )
    ]
    news_provider.return_value = provider_response({"status": "ok", "news": entries})
    response = news_client.get("/api/v1/news?feed=housing")
    assert response.status_code == 200
    assert [article["title"] for article in response.json()] == [
        e["title"] for e in entries[:4]
    ]
    assert news_provider.call_args.kwargs["params"]["keywords"] == "mortgage"
    news_provider.assert_awaited_once()
