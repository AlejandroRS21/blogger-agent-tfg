"""Retry and backoff policies for continuous publishing."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, Optional, Sequence, TypeVar
import time

T = TypeVar("T")


@dataclass
class RetryPolicy:
    """Simple bounded retry policy with custom backoff schedule."""

    max_retries: int = 3
    backoff_seconds: Sequence[float] = (300.0, 900.0, 1800.0)
    sleeper: Callable[[float], None] = time.sleep

    def get_backoff(self, attempt: int) -> float:
        """Return backoff for the given retry attempt index (1-based)."""
        if attempt <= 0:
            return 0.0
        if attempt <= len(self.backoff_seconds):
            return float(self.backoff_seconds[attempt - 1])
        return float(self.backoff_seconds[-1]) if self.backoff_seconds else 0.0

    def run(self, fn: Callable[[], T], retriable: Optional[Callable[[Exception], bool]] = None) -> T:
        """Execute a function with retries according to policy."""
        attempts = 0
        while True:
            try:
                return fn()
            except Exception as exc:  # noqa: BLE001
                attempts += 1
                can_retry = attempts <= self.max_retries
                if retriable and not retriable(exc):
                    raise
                if not can_retry:
                    raise
                self.sleeper(self.get_backoff(attempts))

    def iter_backoff_schedule(self) -> Iterable[float]:
        """Expose finite backoff schedule used by current policy."""
        for idx in range(1, self.max_retries + 1):
            yield self.get_backoff(idx)
