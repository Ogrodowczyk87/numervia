"""Explicit YouTube refresh; one durable reservation for each search request."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email.utils import parsedate_to_datetime
from html import unescape
from uuid import uuid4

import httpx

from app.video_state import (
    CATEGORIES,
    Category,
    SavedCategory,
    Video,
    VideoAttempt,
    VideoFeed,
    VideoSnapshot,
    VideoState,
)
from app.video_store import FileVideoStore

INTERVAL = timedelta(hours=6)
DAY = timedelta(hours=24)
TOLERANCE = timedelta(minutes=5)
QUERIES: dict[Category, str] = {
    "Finance": "personal finance investing explained",
    "Economy": "economy economics news explained",
    "Technology": "technology innovation news explained",
}


def utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone is required")
    return value.astimezone(UTC)


def slot_at(value: datetime) -> datetime:
    value = utc(value)
    return value.replace(hour=value.hour // 6 * 6, minute=0, second=0, microsecond=0)


def retry_delay(value: str | None, now: datetime) -> timedelta:
    try:
        return max(INTERVAL, timedelta(seconds=int(value or "")))
    except ValueError, OverflowError:
        try:
            return max(INTERVAL, utc(parsedate_to_datetime(value or "")) - now)
        except ValueError, TypeError, OverflowError:
            return INTERVAL


async def fetch_live(category: Category, token: str, now: datetime) -> list[Video]:
    async with httpx.AsyncClient(timeout=10, follow_redirects=False) as client:
        response = await client.get(
            "https://www.googleapis.com/youtube/v3/search",
            headers={"X-Goog-Api-Key": token},
            params={
                "part": "snippet",
                "type": "video",
                "q": QUERIES[category],
                "maxResults": 5,
                "relevanceLanguage": "en",
                "safeSearch": "strict",
                "videoEmbeddable": "true",
                "videoSyndicated": "true",
                "order": "relevance",
                "publishedAfter": (utc(now) - timedelta(days=30)).isoformat(),
            },
        )
    response.raise_for_status()
    items = response.json()["items"]
    if not isinstance(items, list):
        raise TypeError("Invalid video response")
    videos, seen = [], set()
    for item in items:
        snippet = item["snippet"]
        thumbnails = snippet["thumbnails"]
        thumbnail = thumbnails.get("high") or thumbnails["default"]
        video = Video(
            video_id=item["id"]["videoId"],
            title=unescape(snippet["title"]),
            channel=unescape(snippet["channelTitle"]),
            thumbnail_url=thumbnail["url"],
            published_at=snippet["publishedAt"],
            category=category,
        )
        if video.video_id not in seen and len(videos) < 2:
            videos.append(video)
            seen.add(video.video_id)
    return videos


@dataclass(frozen=True)
class RefreshResult:
    status: str
    attempts: int
    budget_warning: bool


async def refresh_category(
    store: FileVideoStore,
    category: Category,
    scheduled_at: datetime,
    now: datetime,
    fetch: Callable[[Category], Awaitable[list[Video]]],
    *,
    mode: str = "demo",
    clock: Callable[[], datetime] | None = None,
) -> RefreshResult:
    if category not in CATEGORIES:
        raise ValueError("Unknown video category")
    now, scheduled_at = utc(now), utc(scheduled_at)
    reservation = str(uuid4())

    def reserve(state: VideoState) -> RefreshResult:
        if state.mode != mode:
            raise ValueError("Demo and live state cannot be mixed")
        if mode == "live" and (
            state.budget is None or state.quota_confirmed_at is None
        ):
            raise ValueError(
                "Live mode requires an explicit verified quota configuration"
            )
        limit = state.budget.request_budget if state.budget else 12
        state.attempts = [a for a in state.attempts if a.at > now - DAY]
        for record in state.categories.values():
            if record.snapshot and now >= record.snapshot.serve_until:
                record.snapshot = None
        count = len(state.attempts)
        warning = count * 5 >= limit * 4
        if (
            scheduled_at != slot_at(scheduled_at)
            or not scheduled_at <= now <= scheduled_at + TOLERANCE
        ):
            return RefreshResult("skipped", count, warning)
        if state.provider_disabled or (
            state.provider_blocked_until and now < state.provider_blocked_until
        ):
            return RefreshResult("skipped", count, warning)
        record = state.categories.setdefault(category, SavedCategory())
        if (record.last_attempt_slot and scheduled_at <= record.last_attempt_slot) or (
            record.next_attempt_at and now < record.next_attempt_at
        ):
            return RefreshResult("skipped", count, warning)
        if count >= limit:
            return RefreshResult("budget_exhausted", count, True)
        state.attempts.append(
            VideoAttempt(id=reservation, category=category, at=now, slot=scheduled_at)
        )
        record.last_attempt_slot = scheduled_at
        record.next_attempt_at = now + INTERVAL
        record.reservation_id = reservation
        return RefreshResult("reserved", count + 1, (count + 1) * 5 >= limit * 4)

    result = store.update(reserve)
    if result.status != "reserved":
        return result
    snapshot, code, blocked, disabled = None, None, None, False
    try:
        async with asyncio.timeout(12):
            videos = await fetch(category)
        fetched = utc(clock()) if clock else now
        snapshot = VideoSnapshot(
            videos=videos,
            updated_at=fetched,
            fresh_until=fetched + INTERVAL + TOLERANCE,
            serve_until=fetched + DAY,
        )
        if any(v.category != category for v in snapshot.videos):
            raise ValueError("Invalid video category")
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        reasons = set()
        try:
            reasons = {
                entry["reason"] for entry in error.response.json()["error"]["errors"]
            }
        except ValueError, KeyError, TypeError:
            pass
        if status == 403 and reasons & {"quotaExceeded", "dailyLimitExceeded"}:
            code, blocked = "quota", now + DAY
        elif status == 429 or (
            status == 403 and reasons & {"rateLimitExceeded", "userRateLimitExceeded"}
        ):
            code, blocked = (
                "rate_limit",
                now + retry_delay(error.response.headers.get("Retry-After"), now),
            )
        elif status in (401, 403) or (status == 400 and "keyInvalid" in reasons):
            code, disabled = "credentials", True
        else:
            code = "unavailable"
    except httpx.HTTPError, TimeoutError:
        code = "unavailable"
    except ValueError, KeyError, TypeError:
        snapshot, code = None, "invalid_data"
    finished = utc(clock()) if clock else now

    def finish(state: VideoState) -> bool:
        if blocked is not None:
            state.provider_blocked_until = max(
                blocked, state.provider_blocked_until or blocked
            )
        state.provider_disabled = state.provider_disabled or disabled
        if code:
            state.last_error_code = code
        record = state.categories[category]
        accepted = snapshot is not None and record.reservation_id == reservation
        if accepted:
            record.snapshot = snapshot
        for saved in state.categories.values():
            if saved.snapshot and finished >= saved.snapshot.serve_until:
                saved.snapshot = None
        return accepted

    accepted = store.update(finish)
    status = (
        "updated"
        if accepted
        else "superseded"
        if snapshot is not None
        else "provider_error"
    )
    return RefreshResult(status, result.attempts, result.budget_warning)


def read_videos(store: FileVideoStore, now: datetime) -> VideoFeed:
    now = utc(now)
    state = store.read()
    snapshots = [
        record.snapshot
        for record in state.categories.values()
        if record.snapshot
        and record.snapshot.updated_at <= now < record.snapshot.serve_until
    ]
    if not snapshots:
        raise LookupError("No usable video snapshots")
    unique = {}
    for snapshot in snapshots:
        for video in snapshot.videos:
            unique.setdefault(video.video_id, video)
    return VideoFeed(
        videos=list(unique.values()),
        updated_at=min(s.updated_at for s in snapshots),
        fresh_until=min(s.fresh_until for s in snapshots),
        serve_until=min(s.serve_until for s in snapshots),
        stale=len(snapshots) < len(CATEGORIES)
        or any(now >= s.fresh_until for s in snapshots),
        demo=state.mode == "demo",
    )
