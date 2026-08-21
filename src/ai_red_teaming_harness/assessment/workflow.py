"""End-to-end Day 14 final assessment reporting workflow."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..evaluators.engine import evaluate_test_pack
from ..findings.builder import build_findings
from ..loader import load_test_pack
from ..providers.factory import get_provider
from ..risk.scorer import score_stability_records
from ..runner import run_test_pack
from ..stability.analyzer import analyze_stability
from .builder import build_assessment_report
from .reporter import write_assessment_reports


def run_assessment_workflow(
    path: Path,
    provider_name: str,
    output_root: Path = Path("output"),
):
    test_pack = load_test_pack(path)
    provider = get_provider(provider_name)

    executions = run_test_pack(test_pack, provider)
    evaluated = evaluate_test_pack(test_pack, executions)

    stability_records, stability_summary = analyze_stability(
        test_pack,
        evaluated,
    )
    risk_records, risk_summary = score_stability_records(
        stability_records,
        stability_summary,
    )
    findings, findings_summary = build_findings(
        risk_records,
        risk_summary,
    )
    report = build_assessment_report(
        findings,
        findings_summary,
    )

    run_folder = (
        f"ASSESSMENT-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
        f"{uuid4().hex[:8]}"
    )
    output_dir = output_root / run_folder
    write_assessment_reports(output_dir, report)

    return report, output_dir
