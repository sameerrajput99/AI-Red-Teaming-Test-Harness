"""Tests for Day 12 deterministic risk scoring."""

from __future__ import annotations

from pathlib import Path

from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.risk.models import RiskLevel
from ai_red_teaming_harness.risk.reporter import write_risk_reports
from ai_red_teaming_harness.risk.scorer import (
    score_stability_record,
    score_stability_records,
)
from ai_red_teaming_harness.risk.workflow import run_risk_workflow
from ai_red_teaming_harness.models import Category, ControlType, EvaluationVerdict, Severity
from ai_red_teaming_harness.stability.models import (
    StabilityRecord,
    StabilityRunSummary,
    StabilityStatus,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACK = PROJECT_ROOT / "test_packs" / "day12_risk_scoring_pack.yaml"


def _record(
    *,
    severity: Severity,
    status: StabilityStatus,
    passes: int,
    fails: int,
    reviews: int = 0,
    errors: int = 0,
) -> StabilityRecord:
    total = passes + fails + reviews + errors
    seen = []
    if passes:
        seen.append(EvaluationVerdict.PASS)
    if fails:
        seen.append(EvaluationVerdict.FAIL)
    if reviews:
        seen.append(EvaluationVerdict.REVIEW)
    if errors:
        seen.append(EvaluationVerdict.ERROR)
    return StabilityRecord(
        test_id="TST-001",
        title="Synthetic risk scoring test",
        category=Category.PROMPT_LEAKAGE,
        control_type=ControlType.ADVERSARIAL,
        severity=severity,
        total_attempts=total,
        pass_count=passes,
        fail_count=fails,
        review_count=reviews,
        error_count=errors,
        pass_rate_percent=round((passes / total) * 100, 2),
        verdicts_seen=seen,
        status=status,
    )


def test_stable_pass_scores_zero_none() -> None:
    result = score_stability_record(
        _record(
            severity=Severity.CRITICAL,
            status=StabilityStatus.STABLE_PASS,
            passes=4,
            fails=0,
        )
    )
    assert result.risk_score == 0
    assert result.risk_level is RiskLevel.NONE


def test_stable_critical_fail_scores_100_critical() -> None:
    result = score_stability_record(
        _record(
            severity=Severity.CRITICAL,
            status=StabilityStatus.STABLE_FAIL,
            passes=0,
            fails=4,
        )
    )
    assert result.risk_score == 100
    assert result.risk_level is RiskLevel.CRITICAL


def test_flaky_high_severity_gets_instability_uplift() -> None:
    result = score_stability_record(
        _record(
            severity=Severity.HIGH,
            status=StabilityStatus.FLAKY,
            passes=2,
            fails=2,
        )
    )
    assert result.observed_issue_factor_percent == 50.0
    assert result.instability_uplift == 15.0
    assert result.risk_score == 53
    assert result.risk_level is RiskLevel.MEDIUM


def test_risk_records_are_sorted_and_summary_counts_levels() -> None:
    stability_records = [
        _record(
            severity=Severity.HIGH,
            status=StabilityStatus.STABLE_FAIL,
            passes=0,
            fails=2,
        ),
        _record(
            severity=Severity.CRITICAL,
            status=StabilityStatus.STABLE_PASS,
            passes=2,
            fails=0,
        ),
    ]
    stability_records[0].test_id = "TST-001"
    stability_records[1].test_id = "TST-002"
    summary = StabilityRunSummary(
        provider_name="mock-test",
        test_pack_name="Synthetic Risk Pack",
        total_tests=2,
        total_attempts=4,
        stable_pass_count=1,
        stable_issue_count=1,
        flaky_count=0,
        average_pass_rate_percent=50.0,
    )

    records, risk_summary = score_stability_records(stability_records, summary)

    assert records[0].risk_score == 75
    assert records[0].risk_level is RiskLevel.HIGH
    assert risk_summary.high_count == 1
    assert risk_summary.none_count == 1
    assert risk_summary.highest_risk_score == 75


def test_risk_reporter_writes_three_artifacts(tmp_path: Path) -> None:
    records, summary, _ = run_risk_workflow(
        PACK,
        "mock-vulnerable",
        output_root=tmp_path / "workflow-output",
    )
    manual_dir = tmp_path / "manual-report"
    write_risk_reports(manual_dir, records, summary)

    assert (manual_dir / "risk.json").is_file()
    assert (manual_dir / "risk.csv").is_file()
    assert (manual_dir / "risk_summary.json").is_file()


def test_complete_day12_pack_expected_risk_for_mock_providers(tmp_path: Path) -> None:
    vulnerable, vulnerable_summary, _ = run_risk_workflow(
        PACK,
        "mock-vulnerable",
        output_root=tmp_path / "vulnerable",
    )
    hardened, hardened_summary, _ = run_risk_workflow(
        PACK,
        "mock-hardened",
        output_root=tmp_path / "hardened",
    )

    vulnerable_by_id = {record.test_id: record for record in vulnerable}
    assert vulnerable_by_id["RSK-001"].risk_score == 100
    assert vulnerable_by_id["RSK-001"].risk_level is RiskLevel.CRITICAL
    assert vulnerable_by_id["RSK-002"].risk_score == 75
    assert vulnerable_by_id["RSK-002"].risk_level is RiskLevel.HIGH
    assert vulnerable_by_id["RSK-003"].risk_score == 50
    assert vulnerable_by_id["RSK-003"].risk_level is RiskLevel.MEDIUM
    assert vulnerable_by_id["RSK-004"].risk_score == 0
    assert vulnerable_by_id["RSK-004"].risk_level is RiskLevel.NONE
    assert vulnerable_summary.critical_count == 1
    assert vulnerable_summary.high_count == 1
    assert vulnerable_summary.medium_count == 1
    assert vulnerable_summary.none_count == 1

    assert all(record.risk_score == 0 for record in hardened)
    assert hardened_summary.none_count == 4
    assert hardened_summary.highest_risk_score == 0
