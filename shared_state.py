"""Thread‑safe in‑memory store for raw and story logs."""

from __future__ import annotations

import threading
from collections import deque
from typing import Deque

import config


class SharedState:
    """Thread‑safe in‑memory store for raw and story logs."""

    def __init__(self):
        self.raw_log: Deque[str] = deque(maxlen=1000)
        self.story: Deque[str] = deque(maxlen=1000)
        self.lock = threading.Lock()
        self.new_raw_logs_count = 0
        self.new_raw_log_condition = threading.Condition(self.lock)

    # convenience helpers ----------------------------------------------------
    def append_raw(self, entry: str) -> None:
        with self.lock:
            self.raw_log.append(entry)
            self.new_raw_logs_count += 1
            # Notify if enough new logs are available for a summary
            if self.new_raw_logs_count >= config.RAW_LOGS_PER_SUMMARY:
                self.new_raw_log_condition.notify()

    def append_story(self, entry: str) -> None:
        with self.lock:
            self.story.append(entry)

    def recent_raw(self, n: int) -> str:
        with self.lock:
            return "\n".join(list(self.raw_log)[-n:])

    def recent_story(self, n: int) -> str:
        with self.lock:
            return "\n".join(list(self.story)[-n:])

    def wait_for_new_raw_logs(self) -> None:
        with self.lock:
            while self.new_raw_logs_count < config.RAW_LOGS_PER_SUMMARY:
                self.new_raw_log_condition.wait()

    def reset_new_raw_logs_count(self) -> None:
        with self.lock:
            self.new_raw_logs_count = 0
