"""End-to-end Day 12 risk-scoring workflow."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..evaluators.engine import evaluate_test_pack
from ..loader import load_test_pack
from ..providers.factory import get_provider
from ..runner import run_test_pack
from ..stability.analyzer import analyze_stability
from .reporter import write_risk_reports
from .scorer import score_stability_records


def run_risk_workflow(
    path: Path,
    provider_name: str,
    output_root: Path = Path("output"),
):
    test_pack = load_test_pack(path)
    provider = get_provider(provider_name)
    executions = run_test_pack(test_pack, provider)
    evaluated = evaluate_test_pack(test_pack, executions)
    stability_records, stability_summary = analyze_stability(test_pack, evaluated)
    risk_records, risk_summary = score_stability_records(
        stability_records,
        stability_summary,
    )

    run_folder = (
        f"RISK-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
        f"{uuid4().hex[:8]}"
    )
    output_dir = output_root / run_folder
    write_risk_reports(output_dir, risk_records, risk_summary)

    return risk_records, risk_summary, output_dir
