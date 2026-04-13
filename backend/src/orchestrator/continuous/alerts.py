"""Operational alert dispatcher for continuous publishing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class AlertDispatcher:
    """Stores and emits alerts in-memory for current process lifecycle."""

    alerts: List[Dict[str, Any]]

    def emit(self, code: str, message: str, severity: str = "warning", context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        event = {
            "code": code,
            "message": message,
            "severity": severity,
            "context": context or {},
            "detected_at": datetime.now(timezone.utc).isoformat(),
        }
        self.alerts.append(event)
        return event

    def snapshot(self) -> List[Dict[str, Any]]:
        return list(self.alerts)
