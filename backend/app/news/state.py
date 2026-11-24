from datetime import timedelta
from typing import Literal, Self

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

from app.news.providers import Feed, NewsArticle, Provider


class NewsSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    articles: list[NewsArticle]
    fetched_at: AwareDatetime
    fresh_until: AwareDatetime
    serve_until: AwareDatetime

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if not self.fetched_at < self.fresh_until <= self.serve_until:
            raise ValueError("Expected fetched_at < fresh_until <= serve_until")

        if self.serve_until - self.fetched_at > timedelta(hours=24):
            raise ValueError("News cannot be served for more than 24 hours")

        return self


# Provider identifiers are part of the persisted schema, never API keys.
FeedKey = Literal["marketaux:overview", "currents:overview", "currents:housing"]
ErrorCode = Literal["quota", "rate_limit", "credentials", "unavailable", "invalid_data"]


class Attempt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    provider: Provider
    feed: Feed
    at: AwareDatetime
    slot: AwareDatetime


class StoredFeed(BaseModel):
    model_config = ConfigDict(extra="forbid")

    snapshot: NewsSnapshot | None = None
    last_attempt_slot: AwareDatetime | None = None
    next_attempt_at: AwareDatetime | None = None
    reservation_id: str | None = None


class ProviderState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    attempts: list[Attempt] = Field(default_factory=list)
    provider_blocked_until: AwareDatetime | None = None
    provider_disabled: bool = False
    last_error_code: ErrorCode | None = None


class NewsState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    mode: Literal["demo", "live"]
    feeds: dict[FeedKey, StoredFeed] = Field(default_factory=dict)
    providers: dict[Provider, ProviderState] = Field(
        default_factory=lambda: {
            "marketaux": ProviderState(),
            "currents": ProviderState(),
        }
    )

    @model_validator(mode="after")
    def validate_providers(self) -> Self:
        if set(self.providers) != {"marketaux", "currents"}:
            raise ValueError("Both provider budget records must exist")
        for provider, state in self.providers.items():
            if any(attempt.provider != provider for attempt in state.attempts):
                raise ValueError("Attempt belongs to a different provider")
            if provider == "marketaux" and any(
                a.feed != "overview" for a in state.attempts
            ):
                raise ValueError("Unsupported provider feed")
        for key, record in self.feeds.items():
            provider = key.split(":")[0]
            if record.snapshot and any(
                a.provider != provider for a in record.snapshot.articles
            ):
                raise ValueError("Article belongs to a different provider")
        return self
