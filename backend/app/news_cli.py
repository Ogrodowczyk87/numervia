"""Local commands; starting the API never invokes this module."""

import argparse
import asyncio
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.news_providers import NewsArticle
from app.news_refresh import FEEDS, fetch_live, read_feed, refresh_feed, slot_at
from app.news_state import NewsSnapshot, NewsState, StoredFeed
from app.news_store import FileNewsStore

DEFAULT_PATH = Path(__file__).resolve().parents[1] / ".local" / "news-demo.json"


def demo_article(provider: str, feed: str) -> NewsArticle:
    return NewsArticle(
        title=f"Demo news: {feed} example — not a real headline",
        url=f"https://example.com/{provider}/{feed}",
        source="Numervia demo",
        published_at="2026-11-14T00:00:00Z",
        provider=provider,
    )


async def run(args: argparse.Namespace) -> None:
    store = FileNewsStore(args.path)
    now = datetime.now(UTC)
    if args.command == "init-demo":
        state = NewsState(mode="demo")
        for key in FEEDS:
            provider, feed = key.split(":")
            state.feeds[key] = StoredFeed(
                snapshot=NewsSnapshot(
                    articles=[demo_article(provider, feed)],
                    fetched_at=now,
                    fresh_until=now + timedelta(hours=6, minutes=5),
                    serve_until=now + timedelta(hours=24),
                )
            )
        store.initialize(state)
        print("Demo state created; no provider requests were made.")
    elif args.command == "init-live":
        if not args.confirm_quota_ready or args.path == DEFAULT_PATH:
            raise ValueError("Use a separate --path and --confirm-quota-ready")
        store.initialize(NewsState(mode="live"))
        print("Live state initialized. No provider requests were made.")
    elif args.command == "read":
        print(json.dumps(read_feed(store, args.feed, now), indent=2))
    else:
        if args.command == "refresh-live":
            if not args.allow_live:
                raise ValueError("Live requests require --allow-live")
            # Validate credentials before reserving units. Never print them.
            tokens = {
                p: os.environ.get(k, "").strip()
                for p, k in (
                    ("marketaux", "MARKETAUX_API_TOKEN"),
                    ("currents", "CURRENTS_API_KEY"),
                )
            }

            async def fetch(provider, feed):
                return await fetch_live(provider, feed, tokens[provider])

            keys = [key for key in FEEDS if tokens[key.split(":")[0]]]
            if not keys:
                raise ValueError("No provider credentials in environment")
            mode = "live"
        else:

            async def fetch(provider, feed):
                return [demo_article(provider, feed)]

            keys, mode = list(FEEDS), "demo"
        # Only the current schedule window; no catch-up requests.
        scheduled = slot_at(now)
        state = store.read()
        keys.sort(
            key=lambda key: (
                state.feeds[key].snapshot.fetched_at
                if key in state.feeds and state.feeds[key].snapshot
                else datetime.min.replace(tzinfo=UTC)
            )
        )
        for key in keys:
            result = await refresh_feed(
                store,
                key,
                scheduled,
                datetime.now(UTC),
                fetch,
                mode=mode,
                clock=lambda: datetime.now(UTC),
            )
            print(
                json.dumps(
                    {
                        "feed": key,
                        "status": result.status,
                        "attempts": result.attempts,
                        "budget_warning": result.budget_warning,
                    }
                )
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=DEFAULT_PATH)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init-demo")
    commands.add_parser("refresh-demo")
    live_init = commands.add_parser("init-live")
    live_init.add_argument("--confirm-quota-ready", action="store_true")
    live_refresh = commands.add_parser("refresh-live")
    live_refresh.add_argument("--allow-live", action="store_true")
    read = commands.add_parser("read")
    read.add_argument("--feed", choices=("overview", "housing"), default="overview")
    args = parser.parse_args()
    try:
        asyncio.run(run(args))
    except OSError, ValueError, RuntimeError, LookupError:
        # Do not expose provider URLs, tokens or response bodies in errors.
        parser.exit(1, "News operation failed. Check state, mode and configuration.\n")


if __name__ == "__main__":
    main()
