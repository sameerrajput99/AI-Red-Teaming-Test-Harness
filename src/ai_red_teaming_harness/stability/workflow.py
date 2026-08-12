"""End-to-end repeated-run stability workflow."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from ..evaluators.engine import evaluate_test_pack
from ..loader import load_test_pack
from ..providers.factory import get_provider
from ..runner import run_test_pack
from .analyzer import analyze_stability
from .reporter import write_stability_reports


def run_stability_workflow(
    path: Path,
    provider_name: str,
    output_root: Path = Path("output"),
):
    test_pack = load_test_pack(path)
    provider = get_provider(provider_name)
    executions = run_test_pack(test_pack, provider)
    evaluated = evaluate_test_pack(test_pack, executions)
    records, summary = analyze_stability(test_pack, evaluated)

    run_folder = (
        f"STABILITY-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
        f"{uuid4().hex[:8]}"
    )
    output_dir = output_root / run_folder
    write_stability_reports(output_dir, records, summary)

    return records, summary, output_dir
