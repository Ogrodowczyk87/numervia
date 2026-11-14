def test_provider_quota_does_not_block_reading_saved_news(
    news_client, saved_news, news_provider
):
    store, now, save = saved_news
    save()
    store.update(
        lambda state: setattr(
            state.providers["marketaux"], "provider_blocked_until", now
        )
    )
    assert news_client.get("/api/v1/news").status_code == 200
    news_provider.assert_not_awaited()
