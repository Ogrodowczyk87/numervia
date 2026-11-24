from datetime import timedelta

import pytest
from pydantic import ValidationError

from app.videos.state import VideoSnapshot


@pytest.mark.parametrize(
    "fresh,serve,naive",
    [(0, 24, False), (-1, 24, False), (7, 6, False), (6, 25, False), (6, 24, True)],
)
def test_video_snapshot_rejects_invalid_lifetime(saved_videos, fresh, serve, naive):
    now = saved_videos[1]
    if naive:
        now = now.replace(tzinfo=None)
    with pytest.raises(ValidationError):
        VideoSnapshot(
            videos=[],
            updated_at=now,
            fresh_until=now + timedelta(hours=fresh),
            serve_until=now + timedelta(hours=serve),
        )
