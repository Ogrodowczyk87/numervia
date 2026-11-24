import asyncio
from unittest.mock import AsyncMock

import httpx
import pytest

from app.news.preview import prepare_preview
from app.news.store import FileNewsStore


def test_failed_preview_preserves_reservation_and_does_not_activate(tmp_path):
    path, marker = tmp_path / "live.json", tmp_path / "enabled"
    fetcher = AsyncMock(side_effect=httpx.ConnectError("Simulated connection failure"))

    with pytest.raises(ValueError, match="No usable headlines"):
        asyncio.run(prepare_preview(
            allow_live=True, confirm_quota_ready=True,
            path=path, marker=marker,
            tokens={"marketaux": "test-token"}, fetcher=fetcher,
        ))

    assert len(FileNewsStore(path).read().providers["marketaux"].attempts) == 1
    assert not marker.exists()
    fetcher.assert_awaited_once()
