"""Tests for Day 5 baseline-versus-candidate comparison behavior."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from ai_red_teaming_harness.comparisons.engine import compare_evaluated_records
from ai_red_teaming_harness.comparisons.summary import build_comparison_summary
from ai_red_teaming_harness.comparisons.workflow import generate_comparison_artifacts
from ai_red_teaming_harness.evaluators.engine import evaluate_test_pack
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.models import ComparisonOutcome
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PACK = PROJECT_ROOT / "test_packs" / "day1_test_cases.yaml"


def _evaluated(provider_name: str):
    pack = load_test_pack(VALID_PACK)
    executions = run_test_pack(pack, get_provider(provider_name))
    return pack, evaluate_test_pack(pack, executions)


def _baseline_candidate():
    pack, baseline = _evaluated("mock-vulnerable")
    _, candidate = _evaluated("mock-hardened")
    return pack, baseline, candidate


def test_comparison_marks_improvements_and_unchanged_pass() -> None:
    pack, baseline, candidate = _baseline_candidate()

    records = compare_evaluated_records(pack, baseline, candidate)

    assert [record.outcome for record in records] == [
        ComparisonOutcome.IMPROVED,
        ComparisonOutcome.IMPROVED,
        ComparisonOutcome.UNCHANGED_PASS,
    ]


def test_reverse_comparison_marks_regressions() -> None:
    pack, vulnerable = _evaluated("mock-vulnerable")
    _, hardened = _evaluated("mock-hardened")

    records = compare_evaluated_records(pack, hardened, vulnerable)

    assert records[0].outcome is ComparisonOutcome.REGRESSED
    assert records[1].outcome is ComparisonOutcome.REGRESSED
    assert records[2].outcome is ComparisonOutcome.UNCHANGED_PASS


def test_comparison_summary_counts_outcomes_and_verdicts() -> None:
    pack, baseline, candidate = _baseline_candidate()
    records = compare_evaluated_records(pack, baseline, candidate)

    summary = build_comparison_summary(pack, records)

    assert summary.total_comparisons == 3
    assert summary.improved_count == 2
    assert summary.regressed_count == 0
    assert summary.unchanged_pass_count == 1
    assert summary.baseline_fail_count == 2
    assert summary.candidate_pass_count == 3


def test_comparison_rejects_mismatched_record_sets() -> None:
    pack, baseline, candidate = _baseline_candidate()

    with pytest.raises(ValueError, match="Candidate records do not match"):
        compare_evaluated_records(pack, baseline, candidate[:-1])


def test_comparison_workflow_creates_all_artifacts(tmp_path: Path) -> None:
    pack, baseline, candidate = _baseline_candidate()

    artifacts = generate_comparison_artifacts(
        pack,
        baseline,
        candidate,
        output_root=tmp_path,
    )

    assert artifacts.output_directory.name.startswith("COMPARE-")
    assert artifacts.json_report.exists()
    assert artifacts.csv_report.exists()
    assert artifacts.summary_report.exists()


def test_comparison_artifacts_preserve_side_by_side_evidence(tmp_path: Path) -> None:
    pack, baseline, candidate = _baseline_candidate()
    artifacts = generate_comparison_artifacts(pack, baseline, candidate, tmp_path)

    payload = json.loads(artifacts.json_report.read_text(encoding="utf-8"))
    with artifacts.csv_report.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert payload["summary"]["improved_count"] == 2
    assert payload["comparisons"][0]["baseline_verdict"] == "FAIL"
    assert payload["comparisons"][0]["candidate_verdict"] == "PASS"
    assert rows[0]["outcome"] == "IMPROVED"
    assert rows[2]["outcome"] == "UNCHANGED_PASS"
