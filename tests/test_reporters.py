"""Tests for Day 4 JSON, CSV and summary evidence reporting."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from ai_red_teaming_harness.evaluators.engine import evaluate_test_pack
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.reporters.csv_reporter import CsvReportWriter
from ai_red_teaming_harness.reporters.json_reporter import JsonReportWriter
from ai_red_teaming_harness.reporters.summary import build_run_summary
from ai_red_teaming_harness.reporters.workflow import generate_report_artifacts
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PACK = PROJECT_ROOT / "test_packs" / "day1_test_cases.yaml"


def _evaluated(provider_name: str = "mock-vulnerable"):
    pack = load_test_pack(VALID_PACK)
    executions = run_test_pack(pack, get_provider(provider_name))
    return pack, evaluate_test_pack(pack, executions)


def test_summary_counts_vulnerable_verdicts() -> None:
    pack, records = _evaluated("mock-vulnerable")

    summary = build_run_summary(pack, records)

    assert summary.total_tests == 3
    assert summary.pass_count == 1
    assert summary.fail_count == 2
    assert summary.review_count == 0
    assert summary.error_count == 0


def test_json_report_preserves_nested_findings(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-vulnerable")
    summary = build_run_summary(pack, records)
    path = JsonReportWriter().write(
        tmp_path / "results.json",
        pack,
        records,
        summary,
    )

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["schema_version"] == "1.0"
    assert payload["summary"]["fail_count"] == 2
    assert payload["results"][0]["security_verdict"] == "FAIL"
    assert payload["results"][0]["findings"][0]["evaluator_type"] == "forbidden_patterns"


def test_csv_report_writes_one_flat_row_per_result(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-hardened")
    summary = build_run_summary(pack, records)
    path = CsvReportWriter().write(
        tmp_path / "results.csv",
        pack,
        records,
        summary,
    )

    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 3
    assert rows[0]["test_id"] == "PL-001"
    assert rows[0]["security_verdict"] == "PASS"
    assert rows[0]["category"] == "prompt_leakage"
    assert "forbidden_patterns" in rows[0]["evaluator_types"]


def test_generate_report_artifacts_creates_all_files(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-vulnerable")

    artifacts = generate_report_artifacts(pack, records, tmp_path)

    assert artifacts.output_directory.name == records[0].execution.run_id
    assert artifacts.json_report.exists()
    assert artifacts.csv_report.exists()
    assert artifacts.summary_report.exists()


def test_summary_json_is_compact_and_matches_run(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-hardened")

    artifacts = generate_report_artifacts(pack, records, tmp_path)
    payload = json.loads(artifacts.summary_report.read_text(encoding="utf-8"))

    assert payload["run_id"] == records[0].execution.run_id
    assert payload["provider_name"] == "mock-hardened"
    assert payload["pass_count"] == 3
    assert "results" not in payload
