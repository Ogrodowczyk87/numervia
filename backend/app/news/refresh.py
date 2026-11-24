"""Controlled refresh: reserve durably before any provider request."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from uuid import uuid4

import httpx

from app.content.readers import NewsReader
from app.news.providers import (
    Feed,
    NewsArticle,
    Provider,
    is_housing_headline,
    parse_articles,
    request_news,
)
from app.news.state import Attempt, FeedKey, NewsSnapshot, NewsState, StoredFeed
from app.news.store import FileNewsStore

INTERVAL = timedelta(hours=6)
DAY = timedelta(hours=24)
TOLERANCE = timedelta(minutes=5)
FEEDS: tuple[FeedKey, ...] = (
    "marketaux:overview",
    "currents:overview",
    "currents:housing",
)
LIMITS: dict[Provider, int] = {"marketaux": 80, "currents": 200}
WARN_AT: dict[Provider, int] = {"marketaux": 60, "currents": 150}


@dataclass(frozen=True)
class RefreshResult:
    status: str
    attempts: int
    budget_warning: bool


def utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone is required")
    return value.astimezone(UTC)


def slot_at(now: datetime) -> datetime:
    now = utc(now)
    return now.replace(hour=now.hour // 6 * 6, minute=0, second=0, microsecond=0)


def retry_after(value: str | None, now: datetime) -> timedelta:
    try:
        seconds = int(value or "")
        return max(INTERVAL, timedelta(seconds=seconds))
    except ValueError, OverflowError:
        try:
            return max(INTERVAL, utc(parsedate_to_datetime(value or "")) - now)
        except ValueError, TypeError, OverflowError:
            return INTERVAL


async def fetch_live(provider: Provider, feed: Feed, token: str) -> list[NewsArticle]:
    # HTTPX does not retry or follow redirects by default.
    async with httpx.AsyncClient(timeout=10, follow_redirects=False) as client:
        response = await request_news(client, provider, token, feed)
    response.raise_for_status()
    articles = parse_articles(provider, response.json())
    if feed == "housing":
        articles = [a for a in articles if is_housing_headline(a.title)]
    return articles


async def refresh_feed(
    store: FileNewsStore,
    key: FeedKey,
    scheduled_at: datetime,
    now: datetime,
    fetch: Callable[[Provider, Feed], Awaitable[list[NewsArticle]]],
    *,
    mode: str = "demo",
    clock: Callable[[], datetime] | None = None,
    manual: bool = False,
) -> RefreshResult:
    if key not in FEEDS:
        raise ValueError("Unknown feed")
    now, scheduled_at = utc(now), utc(scheduled_at)
    provider, feed = key.split(":")
    reservation = str(uuid4())

    def reserve(state: NewsState) -> RefreshResult:
        if state.mode != mode:
            raise ValueError("Demo and live state cannot be mixed")
        for record in state.feeds.values():
            if record.snapshot and now >= record.snapshot.serve_until:
                record.snapshot = None
        budget = state.providers[provider]
        # Fail closed on a backwards clock; never prune future reservations.
        budget.attempts = [a for a in budget.attempts if a.at > now - DAY]
        count = len(budget.attempts)
        result = RefreshResult("skipped", count, count >= WARN_AT[provider])
        # Explicit local preview can run outside the schedule window. All durable
        # budget, cooldown, slot deduplication and provider block checks still apply.
        if scheduled_at != slot_at(scheduled_at) or not (
            scheduled_at <= now <= scheduled_at + TOLERANCE
            or manual and mode == "live" and scheduled_at == slot_at(now)
        ):
            return result
        if budget.provider_disabled or (
            budget.provider_blocked_until and now < budget.provider_blocked_until
        ):
            return result
        stored = state.feeds.setdefault(key, StoredFeed())
        if (stored.last_attempt_slot and scheduled_at <= stored.last_attempt_slot) or (
            stored.next_attempt_at and now < stored.next_attempt_at
        ):
            return result
        if count >= LIMITS[provider]:
            return RefreshResult("budget_exhausted", count, True)
        budget.attempts.append(
            Attempt(
                id=reservation, provider=provider, feed=feed, at=now, slot=scheduled_at
            )
        )
        stored.last_attempt_slot = scheduled_at
        stored.next_attempt_at = now + INTERVAL
        stored.reservation_id = reservation
        count += 1
        return RefreshResult("reserved", count, count >= WARN_AT[provider])

    reserved = store.update(reserve)
    if reserved.status != "reserved":
        return reserved

    error_code = None
    blocked_until = None
    disabled = False
    snapshot = None
    try:
        async with asyncio.timeout(12):
            articles = await fetch(provider, feed)
        fetched_at = utc(clock()) if clock else now
        snapshot = NewsSnapshot(
            articles=articles,
            fetched_at=fetched_at,
            fresh_until=fetched_at + INTERVAL + TOLERANCE,
            serve_until=fetched_at + DAY,
        )
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        if status == 402:
            error_code, blocked_until = "quota", now + DAY
        elif status == 429:
            error_code = "rate_limit"
            blocked_until = now + retry_after(
                error.response.headers.get("Retry-After"), now
            )
        elif status in (401, 403):
            error_code, disabled = "credentials", True
        else:
            error_code = "unavailable"
    except httpx.HTTPError, TimeoutError:
        error_code = "unavailable"
    except ValueError, TypeError, KeyError:
        error_code = "invalid_data"

    finished_at = utc(clock()) if clock else now

    def finish(state: NewsState) -> bool:
        # Merge into the current state; do not overwrite concurrent reservations.
        budget = state.providers[provider]
        if blocked_until is not None:
            budget.provider_blocked_until = max(
                blocked_until, budget.provider_blocked_until or blocked_until
            )
        budget.provider_disabled = budget.provider_disabled or disabled
        if error_code:
            budget.last_error_code = error_code
        stored = state.feeds[key]
        accepted = stored.reservation_id == reservation and snapshot is not None
        if accepted:
            stored.snapshot = snapshot
        for record in state.feeds.values():
            if record.snapshot and finished_at >= record.snapshot.serve_until:
                record.snapshot = None
        return accepted

    accepted = store.update(finish)
    return RefreshResult(
        "updated"
        if accepted
        else "superseded"
        if snapshot is not None
        else "provider_error",
        reserved.attempts,
        reserved.budget_warning,
    )


def read_feed(store: NewsReader, feed: Feed, now: datetime) -> dict:
    """Pure read: no HTTP, credentials, budget changes or implicit initialization."""
    now = utc(now)
    if feed not in ("overview", "housing"):
        raise ValueError("Unknown feed")
    state = store.read()
    snapshots = [
        record.snapshot
        for key, record in state.feeds.items()
        if key.endswith(":" + feed)
        and record.snapshot is not None
        and record.snapshot.fetched_at <= now < record.snapshot.serve_until
    ]
    if not snapshots:
        raise LookupError("No usable news snapshot")
    unique = {}
    for snapshot in snapshots:
        for article in snapshot.articles:
            unique.setdefault(str(article.url).split("#", 1)[0], article)
    return {
        "articles": [a.model_dump(mode="json") for a in unique.values()],
        "feed": feed,
        "fetched_at": min(s.fetched_at for s in snapshots).isoformat(),
        "fresh_until": min(s.fresh_until for s in snapshots).isoformat(),
        "serve_until": min(s.serve_until for s in snapshots).isoformat(),
        "stale": any(now >= s.fresh_until for s in snapshots),
        "demo": state.mode == "demo",
    }
