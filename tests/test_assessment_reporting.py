"""Tests for Day 14 consolidated assessment reporting."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ai_red_teaming_harness.assessment.builder import build_assessment_report
from ai_red_teaming_harness.assessment.models import AssessmentPosture
from ai_red_teaming_harness.assessment.reporter import write_assessment_reports
from ai_red_teaming_harness.assessment.workflow import run_assessment_workflow
from ai_red_teaming_harness.findings.models import (
    FindingStatus,
    FindingsRunSummary,
    SecurityFinding,
)
from ai_red_teaming_harness.models import Category, ControlType, Severity
from ai_red_teaming_harness.risk.models import RiskLevel
from ai_red_teaming_harness.stability.models import StabilityStatus


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACK = PROJECT_ROOT / "test_packs" / "day12_risk_scoring_pack.yaml"


def _summary(
    *,
    total_findings: int,
    low: int = 0,
    medium: int = 0,
    high: int = 0,
    critical: int = 0,
    highest: int = 0,
) -> FindingsRunSummary:
    return FindingsRunSummary(
        provider_name="mock-test",
        test_pack_name="Synthetic Assessment Pack",
        total_tests_assessed=4,
        total_findings=total_findings,
        low_count=low,
        medium_count=medium,
        high_count=high,
        critical_count=critical,
        high_or_critical_count=high + critical,
        highest_risk_score=highest,
        generated_at=datetime.now(timezone.utc),
    )


def _finding(
    *,
    finding_id: str,
    test_id: str,
    score: int,
    level: RiskLevel,
    severity: Severity,
    title: str = "Synthetic observed security finding",
) -> SecurityFinding:
    return SecurityFinding(
        finding_id=finding_id,
        test_id=test_id,
        title=title,
        provider_name="mock-test",
        category=Category.PROMPT_LEAKAGE,
        control_type=ControlType.ADVERSARIAL,
        severity=severity,
        risk_score=score,
        risk_level=level,
        stability_status=StabilityStatus.STABLE_FAIL,
        pass_rate_percent=0.0,
        observed_issue_factor_percent=100.0,
        status=FindingStatus.OPEN,
        observation="A synthetic issue was observed during deterministic test execution.",
        impact="Protected information could be exposed if this behavior occurs in a real system.",
        recommendation="Preserve trusted instruction boundaries and retest after remediation.",
        evidence_summary="Issue factor 100%; pass rate 0%; stability STABLE_FAIL.",
        created_at=datetime.now(timezone.utc),
    )


def test_no_findings_produces_no_observed_findings_posture() -> None:
    report = build_assessment_report(
        [],
        _summary(total_findings=0, highest=0),
    )

    assert report.posture is AssessmentPosture.NO_OBSERVED_FINDINGS
    assert report.prioritized_actions == []
    assert "does not constitute a full security certification" in report.executive_summary


def test_highest_finding_controls_observed_posture() -> None:
    medium = _finding(
        finding_id="FND-TST-001",
        test_id="TST-001",
        score=50,
        level=RiskLevel.MEDIUM,
        severity=Severity.MEDIUM,
    )
    critical = _finding(
        finding_id="FND-TST-002",
        test_id="TST-002",
        score=100,
        level=RiskLevel.CRITICAL,
        severity=Severity.CRITICAL,
    )

    report = build_assessment_report(
        [medium, critical],
        _summary(
            total_findings=2,
            medium=1,
            critical=1,
            highest=100,
        ),
    )

    assert report.posture is AssessmentPosture.CRITICAL
    assert report.findings_summary.high_or_critical_count == 1


def test_prioritized_actions_include_finding_ids() -> None:
    finding = _finding(
        finding_id="FND-TST-001",
        test_id="TST-001",
        score=75,
        level=RiskLevel.HIGH,
        severity=Severity.HIGH,
    )

    report = build_assessment_report(
        [finding],
        _summary(
            total_findings=1,
            high=1,
            highest=75,
        ),
    )

    assert len(report.prioritized_actions) == 1
    assert report.prioritized_actions[0].startswith("FND-TST-001 (HIGH 75/100)")


def test_reporter_writes_json_markdown_and_html(tmp_path: Path) -> None:
    finding = _finding(
        finding_id="FND-TST-001",
        test_id="TST-001",
        score=75,
        level=RiskLevel.HIGH,
        severity=Severity.HIGH,
    )
    report = build_assessment_report(
        [finding],
        _summary(
            total_findings=1,
            high=1,
            highest=75,
        ),
    )

    write_assessment_reports(tmp_path, report)

    assert (tmp_path / "assessment_report.json").is_file()
    assert (tmp_path / "assessment_report.md").is_file()
    assert (tmp_path / "assessment_report.html").is_file()


def test_html_report_escapes_finding_text(tmp_path: Path) -> None:
    finding = _finding(
        finding_id="FND-TST-001",
        test_id="TST-001",
        score=50,
        level=RiskLevel.MEDIUM,
        severity=Severity.MEDIUM,
        title="Synthetic <script>alert(1)</script> finding",
    )
    report = build_assessment_report(
        [finding],
        _summary(
            total_findings=1,
            medium=1,
            highest=50,
        ),
    )

    write_assessment_reports(tmp_path, report)
    html = (tmp_path / "assessment_report.html").read_text(encoding="utf-8")

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html


def test_complete_day14_workflow_for_vulnerable_and_hardened(
    tmp_path: Path,
) -> None:
    vulnerable, _ = run_assessment_workflow(
        PACK,
        "mock-vulnerable",
        output_root=tmp_path / "vulnerable",
    )
    hardened, _ = run_assessment_workflow(
        PACK,
        "mock-hardened",
        output_root=tmp_path / "hardened",
    )

    assert vulnerable.posture is AssessmentPosture.CRITICAL
    assert vulnerable.findings_summary.total_findings == 3
    assert vulnerable.findings_summary.highest_risk_score == 100

    assert hardened.posture is AssessmentPosture.NO_OBSERVED_FINDINGS
    assert hardened.findings_summary.total_findings == 0
    assert hardened.findings_summary.highest_risk_score == 0
