"""Operational monitoring and SLI/SLO evaluation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .alerts import AlertDispatcher
from .history_store import HistoryStore


@dataclass
class OperationalMonitor:
    """Evaluates SLI/SLO thresholds and emits operational alerts."""

    history_store: HistoryStore
    alert_dispatcher: AlertDispatcher
    min_success_rate: float = 0.95
    max_lag_minutes: float = 90.0

    def evaluate(self) -> Dict[str, Any]:
        success_rate = self.history_store.daily_success_rate()
        avg_lag = self.history_store.average_lag_minutes()
        critical_open = self.history_store.count_open_incidents(severity="critical")

        if success_rate < self.min_success_rate:
            self.alert_dispatcher.emit(
                code="SLI_SUCCESS_RATE_BREACH",
                severity="major",
                message="Daily success rate below configured SLO",
                context={"success_rate": success_rate, "target": self.min_success_rate},
            )

        if avg_lag > self.max_lag_minutes:
            self.alert_dispatcher.emit(
                code="SLI_CYCLE_LAG_BREACH",
                severity="major",
                message="Average cycle lag above configured SLO",
                context={"avg_lag_minutes": avg_lag, "target": self.max_lag_minutes},
            )

        if critical_open > 0:
            self.alert_dispatcher.emit(
                code="CRITICAL_INCIDENT_OPEN",
                severity="critical",
                message="Critical incidents remain unresolved",
                context={"critical_open_incidents": critical_open},
            )

        return {
            "success_rate": success_rate,
            "avg_lag_minutes": avg_lag,
            "critical_open_incidents": critical_open,
            "alerts": self.alert_dispatcher.snapshot(),
        }
