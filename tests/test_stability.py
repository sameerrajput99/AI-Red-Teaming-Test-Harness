"""Tests for Day 11 repeated-run stability analysis."""

from __future__ import annotations

from pathlib import Path

from ai_red_teaming_harness.evaluators.engine import evaluate_test_pack
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import run_test_pack
from ai_red_teaming_harness.stability.analyzer import analyze_stability
from ai_red_teaming_harness.stability.models import StabilityStatus
from ai_red_teaming_harness.stability.reporter import write_stability_reports


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACK = PROJECT_ROOT / "test_packs" / "day11_stability_pack.yaml"


def _analyze(provider_name: str):
    test_pack = load_test_pack(PACK)
    executions = run_test_pack(test_pack, get_provider(provider_name))
    evaluated = evaluate_test_pack(test_pack, executions)
    records, summary = analyze_stability(test_pack, evaluated)
    return test_pack, executions, records, summary


def test_day11_pack_executes_ten_total_attempts() -> None:
    _, executions, _, _ = _analyze("mock-hardened")

    assert len(executions) == 10


def test_mock_flaky_marks_repeated_attack_as_flaky() -> None:
    _, _, records, _ = _analyze("mock-flaky")
    record = next(item for item in records if item.test_id == "FLK-001")

    assert record.total_attempts == 4
    assert record.pass_count == 2
    assert record.fail_count == 2
    assert record.pass_rate_percent == 50.0
    assert record.status is StabilityStatus.FLAKY


def test_mock_hardened_is_stable_pass_for_all_tests() -> None:
    _, _, records, summary = _analyze("mock-hardened")

    assert all(
        record.status is StabilityStatus.STABLE_PASS
        for record in records
    )
    assert summary.stable_pass_count == 3
    assert summary.flaky_count == 0
    assert summary.total_attempts == 10


def test_mock_vulnerable_has_one_stable_failure() -> None:
    _, _, records, summary = _analyze("mock-vulnerable")
    attack = next(item for item in records if item.test_id == "FLK-001")

    assert attack.status is StabilityStatus.STABLE_FAIL
    assert attack.pass_rate_percent == 0.0
    assert attack.fail_count == 4
    assert summary.stable_issue_count == 1


def test_flaky_summary_reports_one_flaky_test() -> None:
    _, _, _, summary = _analyze("mock-flaky")

    assert summary.total_tests == 3
    assert summary.total_attempts == 10
    assert summary.stable_pass_count == 2
    assert summary.stable_issue_count == 0
    assert summary.flaky_count == 1


def test_stability_reporter_writes_three_artifacts(tmp_path: Path) -> None:
    _, _, records, summary = _analyze("mock-flaky")

    write_stability_reports(tmp_path, records, summary)

    assert (tmp_path / "stability.json").is_file()
    assert (tmp_path / "stability.csv").is_file()
    assert (tmp_path / "stability_summary.json").is_file()
