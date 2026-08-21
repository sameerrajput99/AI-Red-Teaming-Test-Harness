"""Deterministically convert Day 12 risk records into normalized findings."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from ..models import Category
from ..risk.models import RiskLevel, RiskRecord, RiskRunSummary
from .models import FindingStatus, FindingsRunSummary, SecurityFinding


CATEGORY_GUIDANCE = {
    Category.PROMPT_LEAKAGE: {
        "impact": (
            "Protected system or developer instructions may be exposed, increasing "
            "the chance of follow-on prompt attacks or disclosure of internal controls."
        ),
        "recommendation": (
            "Keep trusted instructions separate from untrusted input, avoid placing "
            "secrets in prompts, and enforce refusal behavior for instruction-disclosure requests."
        ),
    },
    Category.PROMPT_INJECTION: {
        "impact": (
            "Untrusted content may influence behavior outside its intended authority "
            "and cause the model to follow attacker-controlled instructions."
        ),
        "recommendation": (
            "Preserve instruction hierarchy, clearly separate untrusted content from "
            "trusted instructions, and validate tool or action requests before execution."
        ),
    },
    Category.INSTRUCTION_OVERRIDE: {
        "impact": (
            "Higher-priority safeguards may be bypassed or ignored, allowing behavior "
            "that conflicts with the intended security policy."
        ),
        "recommendation": (
            "Enforce trusted instruction precedence and reject requests that attempt "
            "to disable, replace, or override higher-priority security controls."
        ),
    },
    Category.REFUSAL_BEHAVIOR: {
        "impact": (
            "The model may fail to maintain a required boundary when handling a "
            "request that should be refused or safely redirected."
        ),
        "recommendation": (
            "Strengthen refusal policy coverage, test common paraphrases, and provide "
            "safe alternative assistance without exposing protected information."
        ),
    },
    Category.HALLUCINATION: {
        "impact": (
            "Unverified or fabricated information may be presented as factual, which "
            "can reduce trust and lead to incorrect downstream decisions."
        ),
        "recommendation": (
            "Require source verification for factual claims, label uncertainty, and "
            "avoid inventing citations or evidence when a source cannot be verified."
        ),
    },
    Category.SAFETY_BOUNDARY: {
        "impact": (
            "Protected data or restricted operations may cross an intended security "
            "boundary without sufficient authorization or validation."
        ),
        "recommendation": (
            "Keep secrets outside model-visible context, enforce authorization in "
            "deterministic application controls, and validate restricted operations before execution."
        ),
    },
    Category.BENIGN_CONTROL: {
        "impact": (
            "Normal allowed behavior may be degraded, creating a usability or "
            "over-refusal regression for legitimate users."
        ),
        "recommendation": (
            "Adjust safeguards so allowed requests continue to work while preserving "
            "the intended security boundary, then rerun benign regression controls."
        ),
    },
}


def _finding_title(record: RiskRecord) -> str:
    return f"{record.title} — observed security finding"


def build_findings(
    risk_records: list[RiskRecord],
    risk_summary: RiskRunSummary,
) -> tuple[list[SecurityFinding], FindingsRunSummary]:
    """Create one finding for every risk record with a non-zero observed score."""

    now = datetime.now(timezone.utc)
    findings: list[SecurityFinding] = []

    for record in risk_records:
        if record.risk_score == 0 or record.risk_level is RiskLevel.NONE:
            continue

        guidance = CATEGORY_GUIDANCE[record.category]
        observation = (
            f"Test {record.test_id} produced a non-zero observed risk score of "
            f"{record.risk_score}/100 ({record.risk_level.value}) for provider "
            f"{risk_summary.provider_name}."
        )
        evidence_summary = (
            f"Observed issue factor: {record.observed_issue_factor_percent:.2f}%; "
            f"pass rate: {record.pass_rate_percent:.2f}%; "
            f"stability: {record.stability_status.value}; "
            f"severity: {record.severity.value}."
        )

        findings.append(
            SecurityFinding(
                finding_id=f"FND-{record.test_id}",
                test_id=record.test_id,
                title=_finding_title(record),
                provider_name=risk_summary.provider_name,
                category=record.category,
                control_type=record.control_type,
                severity=record.severity,
                risk_score=record.risk_score,
                risk_level=record.risk_level,
                stability_status=record.stability_status,
                pass_rate_percent=record.pass_rate_percent,
                observed_issue_factor_percent=record.observed_issue_factor_percent,
                status=FindingStatus.OPEN,
                observation=observation,
                impact=guidance["impact"],
                recommendation=guidance["recommendation"],
                evidence_summary=evidence_summary,
                created_at=now,
            )
        )

    findings.sort(key=lambda item: (-item.risk_score, item.finding_id))

    counts = Counter(finding.risk_level for finding in findings)
    highest = max((finding.risk_score for finding in findings), default=0)

    summary = FindingsRunSummary(
        provider_name=risk_summary.provider_name,
        test_pack_name=risk_summary.test_pack_name,
        total_tests_assessed=risk_summary.total_tests,
        total_findings=len(findings),
        low_count=counts[RiskLevel.LOW],
        medium_count=counts[RiskLevel.MEDIUM],
        high_count=counts[RiskLevel.HIGH],
        critical_count=counts[RiskLevel.CRITICAL],
        high_or_critical_count=(
            counts[RiskLevel.HIGH] + counts[RiskLevel.CRITICAL]
        ),
        highest_risk_score=highest,
        generated_at=now,
    )

    return findings, summary
