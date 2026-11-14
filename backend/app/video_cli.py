"""Explicit local video initialization, read and scheduled refresh commands."""

import argparse
import asyncio
import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.video_refresh import fetch_live, read_videos, refresh_category, slot_at
from app.video_state import (
    CATEGORIES,
    SavedCategory,
    Video,
    VideoBudget,
    VideoSnapshot,
    VideoState,
)
from app.video_store import FileVideoStore

DEFAULT_PATH = Path(__file__).resolve().parents[1] / ".local" / "videos-demo.json"


def demo_video(category: str, now: datetime) -> Video:
    return Video(
        video_id=f"demo{CATEGORIES.index(category) + 1:07d}",
        title=f"Demo: {category} explained",
        channel="Numervia demo",
        thumbnail_url="https://example.com/demo-preview.jpg",
        published_at=now,
        category=category,
    )


async def run(args: argparse.Namespace) -> None:
    now = datetime.now(UTC)
    store = FileVideoStore(args.path)
    if args.command == "init-demo":
        state = VideoState(mode="demo")
        for category in CATEGORIES:
            state.categories[category] = SavedCategory(
                snapshot=VideoSnapshot(
                    videos=[demo_video(category, now)],
                    updated_at=now,
                    fresh_until=now + timedelta(hours=6, minutes=5),
                    serve_until=now + timedelta(hours=24),
                )
            )
        store.initialize(state)
        print("Demo video state created; no YouTube requests made.")
    elif args.command == "init-live":
        if args.path == DEFAULT_PATH or not args.confirm_quota_ready:
            raise ValueError("Separate live path and quota confirmation required")
        budget = VideoBudget(
            daily_quota=args.daily_quota,
            cost_per_search=args.cost_per_search,
            request_budget=args.request_budget,
        )
        store.initialize(VideoState(mode="live", budget=budget, quota_confirmed_at=now))
        print("Live video state initialized; no YouTube requests made.")
    elif args.command == "read":
        print(read_videos(store, now).model_dump_json(indent=2))
    else:
        mode = "live" if args.command == "refresh-live" else "demo"
        if mode == "live":
            if not args.allow_live:
                raise ValueError("Explicit live opt-in required")
            token = os.getenv("YOUTUBE_API_KEY", "").strip()
            if not token:
                raise ValueError("Missing YouTube key in process environment")

            async def fetch(category):
                return await fetch_live(category, token, datetime.now(UTC))
        else:

            async def fetch(category):
                return [demo_video(category, datetime.now(UTC))]

        state = store.read()
        categories = sorted(
            CATEGORIES,
            key=lambda category: (
                state.categories[category].snapshot.updated_at
                if category in state.categories and state.categories[category].snapshot
                else datetime.min.replace(tzinfo=UTC)
            ),
        )
        scheduled = slot_at(now)
        for category in categories:
            result = await refresh_category(
                store,
                category,
                scheduled,
                datetime.now(UTC),
                fetch,
                mode=mode,
                clock=lambda: datetime.now(UTC),
            )
            print(
                json.dumps(
                    {
                        "category": category,
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
    commands.add_parser("read")
    commands.add_parser("refresh-demo")
    live_init = commands.add_parser("init-live")
    live_init.add_argument("--daily-quota", type=int, required=True)
    live_init.add_argument("--cost-per-search", type=int, required=True)
    live_init.add_argument("--request-budget", type=int, required=True)
    live_init.add_argument("--confirm-quota-ready", action="store_true")
    live_refresh = commands.add_parser("refresh-live")
    live_refresh.add_argument("--allow-live", action="store_true")
    try:
        asyncio.run(run(parser.parse_args()))
    except OSError, ValueError, RuntimeError, LookupError:
        parser.exit(
            1, "Video operation failed. Check state, mode and quota configuration.\n"
        )


if __name__ == "__main__":
    main()
