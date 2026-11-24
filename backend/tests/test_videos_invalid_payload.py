import asyncio

import pytest

from app.videos.refresh import fetch_live


@pytest.mark.parametrize("payload", [{}, {"items": None}, {"items": [{}]}])
def test_videos_invalid_payload(
    video_provider, provider_response, saved_videos, payload
):
    video_provider.return_value = provider_response(payload)
    with pytest.raises((ValueError, TypeError, KeyError)):
        asyncio.run(fetch_live("Finance", "test-key", saved_videos[1]))
