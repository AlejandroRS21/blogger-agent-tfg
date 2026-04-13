"""Trust-boundary controls for external topic sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from html import unescape
from typing import Any, Dict, Iterable, List, Sequence
import re


PROMPT_INJECTION_PATTERNS: Sequence[re.Pattern[str]] = (
    re.compile(r"ignore\s+previous\s+instructions", re.IGNORECASE),
    re.compile(r"system\s+prompt", re.IGNORECASE),
    re.compile(r"developer\s+message", re.IGNORECASE),
    re.compile(r"jailbreak", re.IGNORECASE),
)


@dataclass
class SourceGuard:
    """Normalizes and sanitizes untrusted external payloads."""

    allowed_domains: Sequence[str] = ("api.search.brave.com", "rss", "fallback-rss", "cli", "test")
    max_title_length: int = 180
    max_description_length: int = 1000
    max_candidates: int = 25
    _allowlist: set[str] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._allowlist = {domain.strip().lower() for domain in self.allowed_domains if domain.strip()}

    def _domain_allowed(self, source: str) -> bool:
        normalized = (source or "").strip().lower()
        if not normalized:
            return False
        if normalized in self._allowlist:
            return True
        return any(normalized.endswith(f"/{domain}") or domain in normalized for domain in self._allowlist)

    def _strip_html(self, value: str) -> str:
        cleaned = re.sub(r"<[^>]+>", " ", value or "")
        cleaned = unescape(cleaned)
        cleaned = re.sub(r"\\s+", " ", cleaned).strip()
        return cleaned

    def _neutralize_prompt_injection(self, value: str) -> str:
        sanitized = value
        for pattern in PROMPT_INJECTION_PATTERNS:
            sanitized = pattern.sub("[filtered]", sanitized)
        return sanitized

    def sanitize_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """Apply allowlist + content sanitization to one candidate."""
        source = str(candidate.get("source", "")).strip()
        if not self._domain_allowed(source):
            raise ValueError(f"untrusted_source:{source}")

        title = self._neutralize_prompt_injection(self._strip_html(str(candidate.get("title", ""))))
        description = self._neutralize_prompt_injection(
            self._strip_html(str(candidate.get("description", "")))
        )

        if len(title) > self.max_title_length:
            title = title[: self.max_title_length].rstrip()
        if len(description) > self.max_description_length:
            description = description[: self.max_description_length].rstrip()

        sanitized = dict(candidate)
        sanitized["title"] = title
        sanitized["description"] = description
        sanitized["source"] = source
        return sanitized

    def sanitize_candidates(self, candidates: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sanitize and filter candidate list with deterministic limits."""
        output: List[Dict[str, Any]] = []
        for candidate in candidates:
            try:
                sanitized = self.sanitize_candidate(candidate)
            except ValueError:
                continue
            if not sanitized.get("title"):
                continue
            output.append(sanitized)
            if len(output) >= self.max_candidates:
                break
        return output
