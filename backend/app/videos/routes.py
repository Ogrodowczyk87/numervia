"""Public video endpoint reads saved metadata only; no YouTube credentials."""

import math
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response

from app.videos.refresh import read_videos, slot_at
from app.videos.state import VideoFeed
from app.videos.store import FileVideoStore, VideoStateUnavailable

DEFAULT_PATH = Path(__file__).resolve().parents[2] / ".local" / "videos-demo.json"
router = APIRouter(prefix="/api/v1", tags=["Videos"])


def get_store() -> FileVideoStore:
    value = os.getenv("VIDEOS_STATE_PATH", "").strip()
    return FileVideoStore(Path(value) if value else DEFAULT_PATH)


def current_time() -> datetime:
    return datetime.now(UTC)


@router.get("/videos", response_model=VideoFeed)
def get_videos(
    response: Response,
    store: Annotated[FileVideoStore, Depends(get_store)],
    now: Annotated[datetime, Depends(current_time)],
) -> VideoFeed:
    try:
        result = read_videos(store, now)
    except (VideoStateUnavailable, LookupError) as error:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "videos_unavailable",
                "message": "Videos are temporarily unavailable.",
            },
            headers={
                "Cache-Control": "no-store",
                "Retry-After": str(
                    max(
                        1,
                        math.ceil(
                            (slot_at(now) + timedelta(hours=6) - now).total_seconds()
                        ),
                    )
                ),
            },
        ) from error
    response.headers["Cache-Control"] = "no-store"
    return result
