from typing import Protocol

from app.news.state import NewsState
from app.videos.state import VideoState


class NewsReader(Protocol):
    def read(self) -> NewsState: ...


class VideoReader(Protocol):
    def read(self) -> VideoState: ...