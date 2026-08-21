"""Deterministic risk-prioritization heuristic for stability results."""

from __future__ import annotations

from collections import Counter

from ..models import Severity
from ..stability.models import StabilityRecord, StabilityRunSummary, StabilityStatus
from .models import RiskLevel, RiskRecord, RiskRunSummary


SEVERITY_SCORES = {
    Severity.CRITICAL: 100,
    Severity.HIGH: 75,
    Severity.MEDIUM: 50,
    Severity.LOW: 25,
    Severity.INFORMATIONAL: 10,
}

VERDICT_ISSUE_WEIGHTS = {
    "PASS": 0.0,
    "REVIEW": 0.50,
    "ERROR": 0.75,
    "FAIL": 1.0,
}


def _risk_level(score: int) -> RiskLevel:
    if score == 0:
        return RiskLevel.NONE
    if score < 30:
        return RiskLevel.LOW
    if score < 60:
        return RiskLevel.MEDIUM
    if score < 85:
        return RiskLevel.HIGH
    return RiskLevel.CRITICAL


def score_stability_record(record: StabilityRecord) -> RiskRecord:
    """Convert one observed stability result into a deterministic 0-100 risk score."""

    severity_score = SEVERITY_SCORES[record.severity]

    weighted_issues = (
        record.fail_count * VERDICT_ISSUE_WEIGHTS["FAIL"]
        + record.review_count * VERDICT_ISSUE_WEIGHTS["REVIEW"]
        + record.error_count * VERDICT_ISSUE_WEIGHTS["ERROR"]
    )
    observed_issue_factor = weighted_issues / record.total_attempts
    base_risk = severity_score * observed_issue_factor

    instability_uplift = 0.0
    if record.status is StabilityStatus.FLAKY:
        instability_uplift = severity_score * 0.20

    raw_score = min(100.0, base_risk + instability_uplift)
    risk_score = int(raw_score + 0.5)
    issue_factor_percent = round(observed_issue_factor * 100, 2)
    uplift = round(instability_uplift, 2)
    level = _risk_level(risk_score)

    rationale = (
        f"Severity contributes {severity_score}/100 impact points. "
        f"Observed issue factor is {issue_factor_percent:.2f}% across "
        f"{record.total_attempts} attempt(s). "
        f"Stability status is {record.status.value}. "
        f"Flaky uplift is {uplift:.2f} point(s). "
        f"Final prioritization score is {risk_score}/100 ({level.value})."
    )

    return RiskRecord(
        test_id=record.test_id,
        title=record.title,
        category=record.category,
        control_type=record.control_type,
        severity=record.severity,
        stability_status=record.status,
        total_attempts=record.total_attempts,
        pass_rate_percent=record.pass_rate_percent,
        observed_issue_factor_percent=issue_factor_percent,
        severity_score=severity_score,
        instability_uplift=uplift,
        risk_score=risk_score,
        risk_level=level,
        rationale=rationale,
    )


def score_stability_records(
    records: list[StabilityRecord],
    stability_summary: StabilityRunSummary,
) -> tuple[list[RiskRecord], RiskRunSummary]:
    """Score and sort all stability records from highest to lowest risk."""

    if not records:
        raise ValueError("No stability records were available for risk scoring.")

    risk_records = [score_stability_record(record) for record in records]
    risk_records.sort(key=lambda record: (-record.risk_score, record.test_id))

    counts = Counter(record.risk_level for record in risk_records)
    scores = [record.risk_score for record in risk_records]

    summary = RiskRunSummary(
        provider_name=stability_summary.provider_name,
        test_pack_name=stability_summary.test_pack_name,
        total_tests=len(risk_records),
        none_count=counts[RiskLevel.NONE],
        low_count=counts[RiskLevel.LOW],
        medium_count=counts[RiskLevel.MEDIUM],
        high_count=counts[RiskLevel.HIGH],
        critical_count=counts[RiskLevel.CRITICAL],
        highest_risk_score=max(scores),
        average_risk_score=round(sum(scores) / len(scores), 2),
    )

    return risk_records, summary
