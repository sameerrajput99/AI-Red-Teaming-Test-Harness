"""Build a concise, explainable Day 14 assessment from Day 13 findings."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from ..findings.models import FindingsRunSummary, SecurityFinding
from ..risk.models import RiskLevel
from .models import AssessmentPosture, AssessmentReport


POSTURE_BY_RISK_LEVEL = {
    RiskLevel.LOW: AssessmentPosture.LOW,
    RiskLevel.MEDIUM: AssessmentPosture.MEDIUM,
    RiskLevel.HIGH: AssessmentPosture.HIGH,
    RiskLevel.CRITICAL: AssessmentPosture.CRITICAL,
}


def _posture(findings: list[SecurityFinding]) -> AssessmentPosture:
    if not findings:
        return AssessmentPosture.NO_OBSERVED_FINDINGS

    highest = max(findings, key=lambda item: item.risk_score)
    return POSTURE_BY_RISK_LEVEL[highest.risk_level]


def _executive_summary(
    findings: list[SecurityFinding],
    summary: FindingsRunSummary,
    posture: AssessmentPosture,
) -> str:
    if not findings:
        return (
            f"The configured assessment of {summary.provider_name} evaluated "
            f"{summary.total_tests_assessed} test(s) and produced no normalized "
            "non-zero findings. This is an observed result for the configured "
            "scope and does not constitute a full security certification."
        )

    return (
        f"The configured assessment of {summary.provider_name} evaluated "
        f"{summary.total_tests_assessed} test(s) and produced "
        f"{summary.total_findings} normalized security finding(s). "
        f"{summary.high_or_critical_count} finding(s) are HIGH or CRITICAL. "
        f"The highest observed risk score is {summary.highest_risk_score}/100, "
        f"resulting in an observed assessment posture of {posture.value}."
    )


def _prioritized_actions(findings: list[SecurityFinding]) -> list[str]:
    actions: list[str] = []
    seen: set[str] = set()

    for finding in findings:
        action = (
            f"{finding.finding_id} ({finding.risk_level.value} "
            f"{finding.risk_score}/100): {finding.recommendation}"
        )
        if action not in seen:
            actions.append(action)
            seen.add(action)
        if len(actions) == 5:
            break

    return actions


def build_assessment_report(
    findings: list[SecurityFinding],
    findings_summary: FindingsRunSummary,
) -> AssessmentReport:
    """Create the final consolidated in-memory report model for Day 14."""

    now = datetime.now(timezone.utc)
    posture = _posture(findings)

    methodology = [
        "Load and validate structured AI security test definitions.",
        "Execute the configured provider against each test and repetition.",
        "Evaluate responses using configured deterministic evaluator rules.",
        "Aggregate repeated verdicts into stability metrics and pass rates.",
        "Calculate project-specific deterministic risk-prioritization scores.",
        "Normalize non-zero observed risk into structured security findings.",
    ]

    limitations = [
        "The report covers only the configured test pack, provider behavior, and evaluator rules.",
        "Zero findings do not prove that the assessed system is fully secure.",
        "Automated deterministic evaluators can produce false positives or false negatives.",
        "Observed repeated-run behavior does not guarantee identical future model behavior.",
    ]

    return AssessmentReport(
        report_id=f"ASSESS-{now:%Y%m%dT%H%M%SZ}-{uuid4().hex[:8]}",
        title="AI Red Teaming Security Assessment Report",
        provider_name=findings_summary.provider_name,
        test_pack_name=findings_summary.test_pack_name,
        generated_at=now,
        posture=posture,
        executive_summary=_executive_summary(
            findings,
            findings_summary,
            posture,
        ),
        scope_statement=(
            f"This report summarizes the configured AI red teaming assessment "
            f"for provider '{findings_summary.provider_name}' using test pack "
            f"'{findings_summary.test_pack_name}'. It consolidates observed "
            "test, stability, risk, and normalized finding data."
        ),
        methodology=methodology,
        findings_summary=findings_summary,
        findings=findings,
        prioritized_actions=_prioritized_actions(findings),
        limitations=limitations,
    )
