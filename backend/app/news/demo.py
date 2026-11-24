"""Synthetic preview content; no publisher data or network requests."""

from datetime import UTC, datetime, timedelta

from app.news.providers import Feed, NewsArticle, Provider
from app.news.state import NewsSnapshot, NewsState, StoredFeed

OVERVIEW = (
    "Market briefing: how investors compare growth and income",
    "Inflation explained: what changing prices mean for household budgets",
    "Savings spotlight: balancing an emergency fund and long-term goals",
    "Business outlook: the indicators behind a changing economy",
    "Portfolio basics: why diversification matters over time",
    "Currency watch: how exchange rates affect everyday spending",
)
HOUSING = (
    "Mortgage planning: comparing monthly payments across different rates",
    "First-home checklist: looking beyond the deposit",
    "Overpayment insights: small extra payments and the loan balance",
    "Property budget: allowing room for moving and maintenance costs",
)


def demo_articles(provider: Provider, feed: Feed, now: datetime) -> list[NewsArticle]:
    titles = HOUSING if feed == "housing" else (
        OVERVIEW[:3] if provider == "marketaux" else OVERVIEW[3:]
    )
    return [
        NewsArticle(
            title=title,
            url=f"https://example.com/numervia-demo/{provider}/{feed}/{index}",
            source="Numervia demo",
            published_at=(now - timedelta(minutes=35 * index)).isoformat(),
            provider=provider,
        )
        for index, title in enumerate(titles)
    ]


def demo_article(provider: Provider, feed: Feed) -> NewsArticle:
    return demo_articles(provider, feed, datetime.now(UTC))[0]


def populate_demo(state: NewsState, now: datetime) -> None:
    if state.mode != "demo":
        raise ValueError("Preview content requires a demo state")
    for key in ("marketaux:overview", "currents:overview", "currents:housing"):
        provider, feed = key.split(":")
        record = state.feeds.setdefault(key, StoredFeed())
        record.snapshot = NewsSnapshot(
            articles=demo_articles(provider, feed, now),
            fetched_at=now,
            fresh_until=now + timedelta(hours=6, minutes=5),
            serve_until=now + timedelta(hours=24),
        )
