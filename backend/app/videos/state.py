from datetime import timedelta
from typing import Literal, Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    HttpUrl,
    model_validator,
)

Category = Literal["Finance", "Economy", "Technology"]
CATEGORIES: tuple[Category, ...] = ("Finance", "Economy", "Technology")


class Video(BaseModel):
    video_id: str = Field(pattern=r"^[A-Za-z0-9_-]{11}$")
    title: str
    channel: str
    thumbnail_url: HttpUrl
    published_at: AwareDatetime
    category: Category


class VideoSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")
    videos: list[Video] = Field(max_length=2)
    updated_at: AwareDatetime
    fresh_until: AwareDatetime
    serve_until: AwareDatetime

    @model_validator(mode="after")
    def dates(self) -> Self:
        if not self.updated_at < self.fresh_until <= self.serve_until:
            raise ValueError("Invalid snapshot dates")
        if self.serve_until - self.updated_at > timedelta(hours=24):
            raise ValueError("Maximum video snapshot age is 24 hours")
        return self


class VideoBudget(BaseModel):
    """Explicit account quota and a smaller application request budget."""

    model_config = ConfigDict(extra="forbid")
    daily_quota: int = Field(gt=0, strict=True)
    cost_per_search: int = Field(gt=0, strict=True)
    request_budget: int = Field(ge=12, strict=True)

    @model_validator(mode="after")
    def capacity(self) -> Self:
        # Leave at least 20% of the declared account quota unused.
        if self.request_budget * self.cost_per_search * 5 > self.daily_quota * 4:
            raise ValueError("Request budget exceeds 80% of declared account quota")
        return self


class VideoAttempt(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    category: Category
    at: AwareDatetime
    slot: AwareDatetime


class SavedCategory(BaseModel):
    model_config = ConfigDict(extra="forbid")
    snapshot: VideoSnapshot | None = None
    last_attempt_slot: AwareDatetime | None = None
    next_attempt_at: AwareDatetime | None = None
    reservation_id: str | None = None


class VideoState(BaseModel):
    model_config = ConfigDict(extra="forbid")
    schema_version: Literal[1] = 1
    mode: Literal["demo", "live"]
    budget: VideoBudget | None = None
    quota_confirmed_at: AwareDatetime | None = None
    attempts: list[VideoAttempt] = Field(default_factory=list)
    categories: dict[Category, SavedCategory] = Field(default_factory=dict)
    provider_blocked_until: AwareDatetime | None = None
    provider_disabled: bool = False
    last_error_code: (
        Literal["quota", "rate_limit", "credentials", "unavailable", "invalid_data"]
        | None
    ) = None

    @model_validator(mode="after")
    def check_categories(self) -> Self:
        for category, record in self.categories.items():
            if record.snapshot and any(
                v.category != category for v in record.snapshot.videos
            ):
                raise ValueError("Video belongs to a different category")
        return self


class VideoFeed(BaseModel):
    videos: list[Video]
    updated_at: AwareDatetime
    fresh_until: AwareDatetime
    serve_until: AwareDatetime
    stale: bool
    demo: bool
