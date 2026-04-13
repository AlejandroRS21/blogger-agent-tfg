"""Persistent history storage for cycles, incidents and published records."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


@dataclass
class CycleRecord:
    cycle_id: str
    scheduled_at: str
    started_at: str
    ended_at: Optional[str]
    status: str
    topic: str
    retry_count: int = 0
    reason: Optional[str] = None
    reason_code: Optional[str] = None
    lag_minutes: float = 0.0
    trace: Optional[Dict[str, Any]] = None


@dataclass
class IncidentRecord:
    incident_id: str
    detected_at: str
    severity: str
    stage: str
    reason_code: str
    recovery_action: str
    resolution_status: str = "open"


class HistoryStore:
    """File-backed history storage with a light in-memory cache."""

    def __init__(self, output_dir: str = "backend/outputs") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.output_dir / "continuous_history.json"
        self._state: Dict[str, Any] = {"cycles": [], "incidents": [], "published": []}
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            self._state = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            self._state = {"cycles": [], "incidents": [], "published": []}

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._state, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_cycle(self, record: CycleRecord) -> None:
        self._state.setdefault("cycles", []).append(asdict(record))
        self._save()

    def add_incident(self, record: IncidentRecord) -> None:
        self._state.setdefault("incidents", []).append(asdict(record))
        self._save()

    def add_published(self, article: Dict[str, Any]) -> None:
        self._state.setdefault("published", []).append(article)
        self._save()

    def get_recent_contents(self, days: int = 14) -> List[str]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        items: List[str] = []
        for entry in self._state.get("published", []):
            raw_date = entry.get("published_at")
            try:
                dt = datetime.fromisoformat(raw_date) if raw_date else None
            except Exception:
                dt = None
            if dt and dt >= cutoff:
                items.append(entry.get("content", ""))
        return items

    def daily_success_rate(self) -> float:
        """Compute success ratio over cycles in the last 24 hours."""
        cycles = self._state.get("cycles", [])
        if not cycles:
            return 1.0

        cutoff = datetime.now(timezone.utc) - timedelta(days=1)
        recent = []
        for cycle in cycles:
            raw = cycle.get("scheduled_at")
            try:
                ts = datetime.fromisoformat(raw) if raw else None
            except Exception:
                ts = None
            if ts and ts >= cutoff:
                recent.append(cycle)

        if not recent:
            return 1.0

        successful = [c for c in recent if c.get("status") in {"success", "skipped_with_reason"}]
        return len(successful) / len(recent)

    def average_lag_minutes(self) -> float:
        """Compute average lag for cycles with lag info."""
        lags = [float(c.get("lag_minutes", 0.0)) for c in self._state.get("cycles", []) if c.get("lag_minutes") is not None]
        if not lags:
            return 0.0
        return sum(lags) / len(lags)

    def count_open_incidents(self, severity: Optional[str] = None) -> int:
        """Count open incidents, optionally filtered by severity."""
        incidents = [i for i in self._state.get("incidents", []) if i.get("resolution_status") != "resolved"]
        if severity:
            incidents = [i for i in incidents if i.get("severity") == severity]
        return len(incidents)

    def should_pause_for_quality(self, min_relevance: float = 70.0) -> bool:
        """Trigger auto-pause if weekly relevance < threshold for 2 consecutive weeks."""
        published = self._state.get("published", [])
        if not published:
            return False

        now = datetime.now(timezone.utc)
        weekly_scores: List[float] = []
        for week_idx in (0, 1):
            start = now - timedelta(days=(7 * (week_idx + 1)))
            end = now - timedelta(days=(7 * week_idx))
            values: List[float] = []
            for item in published:
                raw = item.get("published_at")
                try:
                    ts = datetime.fromisoformat(raw) if raw else None
                except Exception:
                    ts = None
                if not ts or ts < start or ts >= end:
                    continue
                score = item.get("relevance_score")
                if score is None:
                    continue
                values.append(float(score))
            if not values:
                return False
            weekly_scores.append(sum(values) / len(values))

        return len(weekly_scores) == 2 and all(score < min_relevance for score in weekly_scores)

    def get_last_cycle(self) -> Optional[Dict[str, Any]]:
        cycles = self._state.get("cycles", [])
        return cycles[-1] if cycles else None

    def get_status_snapshot(self) -> Dict[str, Any]:
        cycles = self._state.get("cycles", [])
        incidents = self._state.get("incidents", [])
        return {
            "total_cycles": len(cycles),
            "total_incidents": len(incidents),
            "last_cycle": cycles[-1] if cycles else None,
            "open_incidents": [i for i in incidents if i.get("resolution_status") != "resolved"],
        }
