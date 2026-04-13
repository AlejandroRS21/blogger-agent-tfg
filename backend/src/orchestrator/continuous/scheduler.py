"""Scheduling utilities for periodic publishing cycles."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass
class ContinuousScheduler:
    """Computes next execution time for fixed publishing cadence."""

    interval_hours: float = 12.0

    def __post_init__(self) -> None:
        if self.interval_hours <= 0:
            raise ValueError("interval_hours must be > 0")

    @property
    def interval(self) -> timedelta:
        return timedelta(hours=self.interval_hours)

    def next_run_at(self, last_run_at: Optional[datetime], now: Optional[datetime] = None) -> datetime:
        """Get next execution datetime from last run or now."""
        current = now or datetime.now(timezone.utc)
        if last_run_at is None:
            return current
        return last_run_at + self.interval

    def should_run_now(self, next_run_at: datetime, now: Optional[datetime] = None) -> bool:
        """True if next run is due at current time."""
        current = now or datetime.now(timezone.utc)
        return current >= next_run_at

    def cycle_lag_minutes(self, scheduled_at: datetime, closed_at: Optional[datetime] = None) -> float:
        """Return positive lag in minutes between schedule and cycle close time."""
        end = closed_at or datetime.now(timezone.utc)
        lag_seconds = (end - scheduled_at).total_seconds()
        return max(lag_seconds / 60.0, 0.0)
