"Tests for Day 6 secure static HTML reporting."

from __future__ import annotations

from pathlib import Path

from ai_red_teaming_harness.comparisons.html_reporter import ComparisonHtmlWriter
from ai_red_teaming_harness.comparisons.workflow import generate_comparison_artifacts
from ai_red_teaming_harness.evaluators.engine import evaluate_test_pack
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.reporters.html_reporter import HtmlReportWriter
from ai_red_teaming_harness.reporters.summary import build_run_summary
from ai_red_teaming_harness.reporters.workflow import generate_report_artifacts
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PACK = PROJECT_ROOT / "test_packs" / "day1_test_cases.yaml"


def _evaluated(provider_name: str):
    pack = load_test_pack(VALID_PACK)
    executions = run_test_pack(pack, get_provider(provider_name))
    return pack, evaluate_test_pack(pack, executions)


def _comparison_inputs():
    pack, baseline = _evaluated("mock-vulnerable")
    _, candidate = _evaluated("mock-hardened")
    return pack, baseline, candidate


def test_run_html_report_contains_summary_and_test_ids(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-vulnerable")
    summary = build_run_summary(pack, records)

    path = HtmlReportWriter().write(
        tmp_path / "results.html",
        pack,
        records,
        summary,
    )
    content = path.read_text(encoding="utf-8")

    assert "Run Evidence Report" in content
    assert "PL-001" in content
    assert "IO-001" in content
    assert "CTRL-001" in content
    assert ">2</strong><span>FAIL" in content


def test_run_html_report_escapes_untrusted_response_markup(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-vulnerable")
    malicious = '<script>alert("evidence")</script>'
    changed_execution = records[0].execution.model_copy(update={"response": malicious})
    changed_record = records[0].model_copy(update={"execution": changed_execution})
    changed_records = [changed_record, *records[1:]]
    summary = build_run_summary(pack, changed_records)

    path = HtmlReportWriter().write(
        tmp_path / "results.html",
        pack,
        changed_records,
        summary,
    )
    content = path.read_text(encoding="utf-8")

    assert malicious not in content
    assert "&lt;script&gt;alert(&quot;evidence&quot;)&lt;/script&gt;" in content
    assert "script-src 'none'" in content


def test_run_workflow_creates_html_artifact(tmp_path: Path) -> None:
    pack, records = _evaluated("mock-hardened")

    artifacts = generate_report_artifacts(pack, records, tmp_path)

    assert artifacts.html_report.exists()
    assert artifacts.html_report.name == "results.html"


def test_comparison_html_contains_outcomes_and_providers(tmp_path: Path) -> None:
    pack, baseline, candidate = _comparison_inputs()
    artifacts = generate_comparison_artifacts(pack, baseline, candidate, tmp_path)
    content = artifacts.html_report.read_text(encoding="utf-8")

    assert "Baseline vs Candidate" in content
    assert "mock-vulnerable" in content
    assert "mock-hardened" in content
    assert "IMPROVED" in content
    assert "UNCHANGED_PASS" in content


def test_comparison_html_escapes_untrusted_side_by_side_evidence(
    tmp_path: Path,
) -> None:
    pack, baseline, candidate = _comparison_inputs()
    artifacts = generate_comparison_artifacts(pack, baseline, candidate, tmp_path)
    first = artifacts.records[0]
    malicious = '<img src=x onerror="alert(1)">'
    changed = first.model_copy(update={"candidate_response": malicious})
    changed_records = [changed, *artifacts.records[1:]]

    path = ComparisonHtmlWriter().write(
        tmp_path / "comparison-safe.html",
        pack,
        changed_records,
        artifacts.summary,
    )
    content = path.read_text(encoding="utf-8")

    assert malicious not in content
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;" in content
    assert "script-src 'none'" in content


def test_comparison_workflow_creates_html_artifact(tmp_path: Path) -> None:
    pack, baseline, candidate = _comparison_inputs()

    artifacts = generate_comparison_artifacts(pack, baseline, candidate, tmp_path)

    assert artifacts.html_report.exists()
    assert artifacts.html_report.name == "comparison.html"
