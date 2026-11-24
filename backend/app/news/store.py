"""Local durable storage. A separate lock survives atomic state replacement."""

import fcntl
import os
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from app.news.state import NewsState

MAX_STATE_BYTES = 1024 * 1024
T = TypeVar("T")


class StateUnavailable(RuntimeError):
    pass


class FileNewsStore:
    def __init__(self, path: Path):
        self.path = path

    def read(self) -> NewsState:
        try:
            with self.path.open("rb") as stream:
                payload = stream.read(MAX_STATE_BYTES + 1)
            if len(payload) > MAX_STATE_BYTES:
                raise ValueError("State too large")
            state = NewsState.model_validate_json(payload)
            # Defaults are useful for explicit initialization, never for recovery
            # of a damaged persisted budget or reservation record.
            records = [state, *state.providers.values(), *state.feeds.values()]
            if any(
                record.model_fields_set != set(type(record).model_fields)
                for record in records
            ):
                raise ValueError("Persisted state has missing fields")
            return state
        except (OSError, ValueError) as error:
            raise StateUnavailable(
                "News state is missing, invalid or unreadable"
            ) from error

    def initialize(self, state: NewsState) -> None:
        """Explicit first creation only; never reset an existing budget."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.with_suffix(self.path.suffix + ".lock").open("a+b") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if self.path.exists():
                raise FileExistsError("News state already exists")
            self._write(state)

    def update(self, change: Callable[[NewsState], T]) -> T:
        """Serialize read-modify-write across local processes, not just threads."""
        try:
            with self.path.with_suffix(self.path.suffix + ".lock").open("a+b") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                state = self.read()
                result = change(state)
                self._write(state)
                return result
        except OSError as error:
            raise StateUnavailable("Could not commit news state") from error

    def _write(self, state: NewsState) -> None:
        payload = state.model_dump_json().encode()
        if len(payload) > MAX_STATE_BYTES:
            raise StateUnavailable("News state exceeds 1 MiB")
        # Revalidate mutations before committing them.
        NewsState.model_validate_json(payload)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                dir=self.path.parent, delete=False
            ) as stream:
                temporary = stream.name
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
            temporary = None
            directory = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if temporary is not None:
                Path(temporary).unlink(missing_ok=True)
