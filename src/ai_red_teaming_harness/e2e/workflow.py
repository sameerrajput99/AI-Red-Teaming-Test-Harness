"""Single-pass integration workflow from YAML input to safe artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4

from ..assessment.builder import build_assessment_report
from ..assessment.reporter import write_assessment_reports
from ..evaluators.engine import evaluate_test_pack
from ..findings.builder import build_findings
from ..loader import load_test_pack
from ..providers.factory import get_provider
from ..risk.scorer import score_stability_records
from ..runner import run_test_pack
from ..stability.analyzer import analyze_stability
from .models import E2ERunResult


ARTIFACT_NAMES = (
    "assessment_report.json",
    "assessment_report.md",
    "assessment_report.html",
    "sanitization_summary.json",
    "e2e_manifest.json",
)


def _write_manifest(output_dir: Path, result_data: dict[str, object]) -> None:
    (output_dir / "e2e_manifest.json").write_text(
        json.dumps(result_data, indent=2),
        encoding="utf-8",
    )


def run_e2e_workflow(
    path: Path,
    provider_name: str,
    output_root: Path = Path("output"),
) -> E2ERunResult:
    """Run every production stage once and preserve its intermediate outputs."""

    test_pack = load_test_pack(path)
    provider = get_provider(provider_name)

    executions = run_test_pack(test_pack, provider)
    evaluations = evaluate_test_pack(test_pack, executions)
    stability_records, stability_summary = analyze_stability(
        test_pack,
        evaluations,
    )
    risk_records, risk_summary = score_stability_records(
        stability_records,
        stability_summary,
    )
    findings, findings_summary = build_findings(
        risk_records,
        risk_summary,
    )
    assessment = build_assessment_report(findings, findings_summary)

    run_folder = (
        f"E2E-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
        f"{uuid4().hex[:8]}"
    )
    output_dir = output_root / run_folder
    write_assessment_reports(output_dir, assessment)

    _write_manifest(
        output_dir,
        {
            "workflow": "day16_end_to_end_v1",
            "provider_name": provider.name,
            "test_pack_name": test_pack.test_pack.name,
            "test_count": len(test_pack.test_cases),
            "execution_count": len(executions),
            "evaluation_count": len(evaluations),
            "stability_record_count": len(stability_records),
            "risk_record_count": len(risk_records),
            "finding_count": len(findings),
            "observed_posture": assessment.posture.value,
            "safe_artifacts": list(ARTIFACT_NAMES[:-1]),
            "raw_prompt_exported": False,
            "raw_response_exported": False,
        },
    )

    return E2ERunResult(
        provider_name=provider.name,
        test_pack_name=test_pack.test_pack.name,
        executions=executions,
        evaluations=evaluations,
        stability_records=stability_records,
        stability_summary=stability_summary,
        risk_records=risk_records,
        risk_summary=risk_summary,
        findings=findings,
        findings_summary=findings_summary,
        assessment=assessment,
        output_dir=output_dir,
        artifact_names=list(ARTIFACT_NAMES),
    )
