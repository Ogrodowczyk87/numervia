import asyncio


def test_news_concurrent_requests(news_provider, news_article, provider_response):
    from app.news import get_news

    async def request(*args, **kwargs):
        await asyncio.sleep(0)
        return provider_response({"data": [news_article]})

    news_provider.side_effect = request

    async def run():
        return await asyncio.gather(*(get_news() for _ in range(10)))

    results = asyncio.run(run())
    assert all(result[0].title == news_article["title"] for result in results)
    news_provider.assert_awaited_once()
