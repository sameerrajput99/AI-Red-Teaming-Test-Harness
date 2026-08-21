"""Recursive deterministic sanitizer for assessment exports."""

from __future__ import annotations

from collections import Counter
from typing import Any

from ..assessment.models import AssessmentReport
from .models import SanitizationSummary
from .policy import DEFAULT_POLICY_NAME, DEFAULT_RULES


def sanitize_text(text: str) -> tuple[str, dict[str, int]]:
    """Redact configured sensitive-text patterns from one string."""

    sanitized = text
    counts: Counter[str] = Counter()

    for rule in DEFAULT_RULES:
        sanitized, replacements = rule.pattern.subn(
            rule.replacement,
            sanitized,
        )
        if replacements:
            counts[rule.name] += replacements

    return sanitized, dict(counts)


def _sanitize_value(
    value: Any,
    counts: Counter[str],
) -> Any:
    if isinstance(value, str):
        sanitized, local_counts = sanitize_text(value)
        counts.update(local_counts)
        return sanitized

    if isinstance(value, list):
        return [_sanitize_value(item, counts) for item in value]

    if isinstance(value, dict):
        return {
            key: _sanitize_value(item, counts)
            for key, item in value.items()
        }

    return value


def sanitize_assessment_report(
    report: AssessmentReport,
) -> tuple[AssessmentReport, SanitizationSummary]:
    """Create a sanitized copy of the full structured assessment report."""

    counts: Counter[str] = Counter()
    raw_data = report.model_dump(mode="json")
    sanitized_data = _sanitize_value(raw_data, counts)

    sanitized_report = AssessmentReport.model_validate(sanitized_data)
    summary = SanitizationSummary(
        policy_name=DEFAULT_POLICY_NAME,
        total_redactions=sum(counts.values()),
        redactions_by_rule=dict(sorted(counts.items())),
        raw_response_exported=False,
        raw_prompt_exported=False,
    )

    return sanitized_report, summary
