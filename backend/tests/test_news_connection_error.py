import pytest


@pytest.mark.parametrize("failure", ["missing", "corrupt", "expired", "empty_state"])
def test_news_unavailable_never_fetches(
    news_client, saved_news, news_provider, failure
):
    store, _, save = saved_news
    if failure == "missing":
        store.path.unlink()
    elif failure == "corrupt":
        store.path.write_text("private-token: invalid JSON")
    elif failure == "expired":
        save(age_hours=24)
    response = news_client.get("/api/v1/news")
    assert response.status_code == 503
    assert response.headers["Cache-Control"] == "no-store"
    assert int(response.headers["Retry-After"]) == 21600
    assert response.json()["detail"]["code"] == (
        "news_not_configured" if failure == "missing" else "news_unavailable"
    )
    assert "private-token" not in response.text
    news_provider.assert_not_awaited()
