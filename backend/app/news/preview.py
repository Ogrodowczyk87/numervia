"""Explicit one-off local preview; API reads never invoke providers."""

import argparse
import asyncio
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from dotenv import dotenv_values

from app.news.refresh import FEEDS, fetch_live, refresh_feed, slot_at
from app.news.state import NewsState
from app.news.store import FileNewsStore

BACKEND_PATH = Path(__file__).resolve().parents[2]
LIVE_PATH = BACKEND_PATH / ".local" / "news-live.json"
PREVIEW_MARKER = BACKEND_PATH / ".local" / "news-preview.enabled"


async def prepare_preview(
    *,
    allow_live: bool,
    confirm_quota_ready: bool,
    path: Path = LIVE_PATH,
    marker: Path = PREVIEW_MARKER,
    tokens: dict[str, str] | None = None,
    fetcher=fetch_live,
) -> None:
    if not allow_live:
        raise ValueError("Explicit live request permission is required")
    if tokens is None:
        # Load credentials only in the explicitly invoked command, never API startup.
        values = dotenv_values(BACKEND_PATH / ".env", interpolate=False)
        tokens = {
            provider: (os.environ.get(key) or values.get(key) or "").strip()
            for provider, key in (
                ("marketaux", "MARKETAUX_API_TOKEN"),
                ("currents", "CURRENTS_API_KEY"),
            )
        }
    keys = [key for key in FEEDS if tokens.get(key.split(":")[0])]
    if not keys:
        raise ValueError("No configured news providers")
    store = FileNewsStore(path)
    if not path.exists():
        if not confirm_quota_ready:
            raise ValueError("First initialization requires quota confirmation")
        store.initialize(NewsState(mode="live"))
    if store.read().mode != "live":
        raise ValueError("Preview requires a separate live ledger")

    async def fetch(provider, feed):
        return await fetcher(provider, feed, tokens[provider])

    for key in keys:
        now = datetime.now(UTC)
        result = await refresh_feed(
            store, key, slot_at(now), now, fetch,
            mode="live", manual=True, clock=lambda: datetime.now(UTC),
        )
        print(json.dumps({"feed": key, "status": result.status, "attempts": result.attempts}))

    now = datetime.now(UTC)
    usable = any(
        record.snapshot and record.snapshot.articles
        and record.snapshot.fetched_at <= now < record.snapshot.serve_until
        for record in store.read().feeds.values()
    )
    if not usable:
        raise ValueError("No usable headlines; ledger preserved for later retry")
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("Local saved news preview enabled.\n")
    print("Saved preview enabled for local API. No automatic provider refresh.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-live", action="store_true")
    parser.add_argument("--confirm-quota-ready", action="store_true")
    args = parser.parse_args()
    try:
        asyncio.run(prepare_preview(
            allow_live=args.allow_live,
            confirm_quota_ready=args.confirm_quota_ready,
        ))
    except (OSError, ValueError, RuntimeError):
        # Never print provider URLs, tokens or response bodies.
        parser.exit(1, "Preview could not be prepared. Check quota, credentials and saved state.\n")


if __name__ == "__main__":
    main()
