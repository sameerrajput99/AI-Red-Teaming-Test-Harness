"""Tests for Day 13 normalized security findings."""

from __future__ import annotations

from pathlib import Path

from ai_red_teaming_harness.findings.builder import build_findings
from ai_red_teaming_harness.findings.models import FindingStatus
from ai_red_teaming_harness.findings.reporter import write_findings_reports
from ai_red_teaming_harness.findings.workflow import run_findings_workflow
from ai_red_teaming_harness.models import Category, ControlType, Severity
from ai_red_teaming_harness.risk.models import RiskLevel, RiskRecord, RiskRunSummary
from ai_red_teaming_harness.stability.models import StabilityStatus


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACK = PROJECT_ROOT / "test_packs" / "day12_risk_scoring_pack.yaml"


def _risk_record(
    *,
    test_id: str,
    category: Category,
    severity: Severity,
    score: int,
    level: RiskLevel,
) -> RiskRecord:
    issue_factor = 0.0 if score == 0 else 100.0
    pass_rate = 100.0 if score == 0 else 0.0
    return RiskRecord(
        test_id=test_id,
        title=f"Synthetic finding test {test_id}",
        category=category,
        control_type=(
            ControlType.BENIGN
            if category is Category.BENIGN_CONTROL
            else ControlType.ADVERSARIAL
        ),
        severity=severity,
        stability_status=(
            StabilityStatus.STABLE_PASS
            if score == 0
            else StabilityStatus.STABLE_FAIL
        ),
        total_attempts=2,
        pass_rate_percent=pass_rate,
        observed_issue_factor_percent=issue_factor,
        severity_score={
            Severity.CRITICAL: 100,
            Severity.HIGH: 75,
            Severity.MEDIUM: 50,
            Severity.LOW: 25,
            Severity.INFORMATIONAL: 10,
        }[severity],
        instability_uplift=0.0,
        risk_score=score,
        risk_level=level,
        rationale="Synthetic risk record for Day 13 unit testing.",
    )


def _risk_summary(total_tests: int) -> RiskRunSummary:
    return RiskRunSummary(
        provider_name="mock-test",
        test_pack_name="Synthetic Findings Pack",
        total_tests=total_tests,
        none_count=0,
        low_count=0,
        medium_count=0,
        high_count=0,
        critical_count=total_tests,
        highest_risk_score=100,
        average_risk_score=100.0,
    )


def test_zero_risk_record_does_not_create_finding() -> None:
    record = _risk_record(
        test_id="TST-001",
        category=Category.BENIGN_CONTROL,
        severity=Severity.INFORMATIONAL,
        score=0,
        level=RiskLevel.NONE,
    )
    summary = RiskRunSummary(
        provider_name="mock-test",
        test_pack_name="Synthetic Findings Pack",
        total_tests=1,
        none_count=1,
        low_count=0,
        medium_count=0,
        high_count=0,
        critical_count=0,
        highest_risk_score=0,
        average_risk_score=0.0,
    )

    findings, findings_summary = build_findings([record], summary)

    assert findings == []
    assert findings_summary.total_findings == 0
    assert findings_summary.highest_risk_score == 0


def test_nonzero_risk_creates_open_normalized_finding() -> None:
    record = _risk_record(
        test_id="TST-001",
        category=Category.PROMPT_LEAKAGE,
        severity=Severity.CRITICAL,
        score=100,
        level=RiskLevel.CRITICAL,
    )

    findings, summary = build_findings([record], _risk_summary(1))
    finding = findings[0]

    assert finding.finding_id == "FND-TST-001"
    assert finding.status is FindingStatus.OPEN
    assert finding.risk_score == 100
    assert summary.total_findings == 1


def test_finding_contains_category_specific_impact_and_recommendation() -> None:
    record = _risk_record(
        test_id="TST-001",
        category=Category.HALLUCINATION,
        severity=Severity.MEDIUM,
        score=50,
        level=RiskLevel.MEDIUM,
    )
    risk_summary = RiskRunSummary(
        provider_name="mock-test",
        test_pack_name="Synthetic Findings Pack",
        total_tests=1,
        none_count=0,
        low_count=0,
        medium_count=1,
        high_count=0,
        critical_count=0,
        highest_risk_score=50,
        average_risk_score=50.0,
    )

    findings, _ = build_findings([record], risk_summary)

    assert "fabricated" in findings[0].impact.lower()
    assert "source verification" in findings[0].recommendation.lower()


def test_findings_are_sorted_by_risk_and_summary_counts_levels() -> None:
    high = _risk_record(
        test_id="TST-002",
        category=Category.SAFETY_BOUNDARY,
        severity=Severity.HIGH,
        score=75,
        level=RiskLevel.HIGH,
    )
    critical = _risk_record(
        test_id="TST-001",
        category=Category.PROMPT_LEAKAGE,
        severity=Severity.CRITICAL,
        score=100,
        level=RiskLevel.CRITICAL,
    )
    risk_summary = RiskRunSummary(
        provider_name="mock-test",
        test_pack_name="Synthetic Findings Pack",
        total_tests=2,
        none_count=0,
        low_count=0,
        medium_count=0,
        high_count=1,
        critical_count=1,
        highest_risk_score=100,
        average_risk_score=87.5,
    )

    findings, summary = build_findings([high, critical], risk_summary)

    assert [item.test_id for item in findings] == ["TST-001", "TST-002"]
    assert summary.critical_count == 1
    assert summary.high_count == 1
    assert summary.high_or_critical_count == 2


def test_findings_reporter_writes_three_artifacts(tmp_path: Path) -> None:
    record = _risk_record(
        test_id="TST-001",
        category=Category.PROMPT_LEAKAGE,
        severity=Severity.CRITICAL,
        score=100,
        level=RiskLevel.CRITICAL,
    )
    findings, summary = build_findings([record], _risk_summary(1))

    write_findings_reports(tmp_path, findings, summary)

    assert (tmp_path / "findings.json").is_file()
    assert (tmp_path / "findings.csv").is_file()
    assert (tmp_path / "findings_summary.json").is_file()


def test_complete_day13_workflow_expected_findings_for_mock_providers(
    tmp_path: Path,
) -> None:
    vulnerable, vulnerable_summary, _ = run_findings_workflow(
        PACK,
        "mock-vulnerable",
        output_root=tmp_path / "vulnerable",
    )
    hardened, hardened_summary, _ = run_findings_workflow(
        PACK,
        "mock-hardened",
        output_root=tmp_path / "hardened",
    )

    assert [finding.test_id for finding in vulnerable] == [
        "RSK-001",
        "RSK-002",
        "RSK-003",
    ]
    assert [finding.risk_score for finding in vulnerable] == [100, 75, 50]
    assert vulnerable_summary.total_findings == 3
    assert vulnerable_summary.high_or_critical_count == 2

    assert hardened == []
    assert hardened_summary.total_findings == 0
    assert hardened_summary.highest_risk_score == 0
