"""Incident management helper for operational events."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
import uuid

from .history_store import HistoryStore, IncidentRecord


@dataclass
class IncidentManager:
    """Creates and tracks operational incidents in the history store."""

    history_store: HistoryStore

    def report(self, stage: str, reason_code: str, severity: str = "warning", recovery_action: str = "retry") -> str:
        incident_id = str(uuid.uuid4())[:8]
        record = IncidentRecord(
            incident_id=incident_id,
            detected_at=datetime.now(timezone.utc).isoformat(),
            severity=severity,
            stage=stage,
            reason_code=reason_code,
            recovery_action=recovery_action,
            resolution_status="open",
        )
        self.history_store.add_incident(record)
        return incident_id

    def resolve(self, incident_id: str) -> None:
        state = self.history_store._state  # Intentionally localized thin mutation helper.
        for incident in state.get("incidents", []):
            if incident.get("incident_id") == incident_id:
                incident["resolution_status"] = "resolved"
                break
        self.history_store._save()
