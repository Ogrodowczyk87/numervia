"""Local durable storage. A separate lock survives atomic state replacement."""

import fcntl
import os
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from app.video_state import VideoState

MAX_STATE_BYTES = 1024 * 1024
T = TypeVar("T")


class VideoStateUnavailable(RuntimeError):
    pass


class FileVideoStore:
    def __init__(self, path: Path):
        self.path = path

    def read(self) -> VideoState:
        try:
            with self.path.open("rb") as stream:
                payload = stream.read(MAX_STATE_BYTES + 1)
            if len(payload) > MAX_STATE_BYTES:
                raise ValueError("State too large")
            state = VideoState.model_validate_json(payload)
            # Defaults are useful for explicit initialization, never for recovery
            # of a damaged persisted budget or reservation record.
            records = [state, *state.categories.values()]
            if state.budget is not None:
                records.append(state.budget)
            if any(
                record.model_fields_set != set(type(record).model_fields)
                for record in records
            ):
                raise ValueError("Persisted state has missing fields")
            return state
        except (OSError, ValueError) as error:
            raise VideoStateUnavailable(
                "Video state is missing, invalid or unreadable"
            ) from error

    def initialize(self, state: VideoState) -> None:
        """Explicit first creation only; never reset an existing budget."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.with_suffix(self.path.suffix + ".lock").open("a+b") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            if self.path.exists():
                raise FileExistsError("Video state already exists")
            self._write(state)

    def update(self, change: Callable[[VideoState], T]) -> T:
        """Serialize read-modify-write across local processes, not just threads."""
        try:
            with self.path.with_suffix(self.path.suffix + ".lock").open("a+b") as lock:
                fcntl.flock(lock, fcntl.LOCK_EX)
                state = self.read()
                result = change(state)
                self._write(state)
                return result
        except OSError as error:
            raise VideoStateUnavailable("Could not commit video state") from error

    def _write(self, state: VideoState) -> None:
        payload = state.model_dump_json().encode()
        if len(payload) > MAX_STATE_BYTES:
            raise VideoStateUnavailable("Video state exceeds 1 MiB")
        # Revalidate mutations before committing them.
        VideoState.model_validate_json(payload)
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
