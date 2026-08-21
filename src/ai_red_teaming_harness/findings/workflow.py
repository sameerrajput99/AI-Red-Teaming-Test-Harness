"""End-to-end Day 13 security findings workflow."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..evaluators.engine import evaluate_test_pack
from ..loader import load_test_pack
from ..providers.factory import get_provider
from ..risk.scorer import score_stability_records
from ..runner import run_test_pack
from ..stability.analyzer import analyze_stability
from .builder import build_findings
from .reporter import write_findings_reports


def run_findings_workflow(
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

    run_folder = (
        f"FINDINGS-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
        f"{uuid4().hex[:8]}"
    )
    output_dir = output_root / run_folder
    write_findings_reports(output_dir, findings, findings_summary)

    return findings, findings_summary, output_dir
