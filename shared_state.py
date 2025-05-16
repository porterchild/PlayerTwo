"""Thread‑safe in‑memory store for raw and story logs."""

from __future__ import annotations

import threading
from collections import deque
from typing import Deque


class SharedState:
    """Thread‑safe in‑memory store for raw and story logs."""

    def __init__(self):
        self.raw_log: Deque[str] = deque(maxlen=1000)
        self.story: Deque[str] = deque(maxlen=1000)
        self.lock = threading.Lock()

    # convenience helpers ----------------------------------------------------
    def append_raw(self, entry: str) -> None:
        with self.lock:
            self.raw_log.append(entry)

    def append_story(self, entry: str) -> None:
        with self.lock:
            self.story.append(entry)

    def recent_raw(self, n: int) -> str:
        with self.lock:
            return "\n".join(list(self.raw_log)[-n:])

    def recent_story(self, n: int) -> str:
        with self.lock:
            return "\n".join(list(self.story)[-n:])
