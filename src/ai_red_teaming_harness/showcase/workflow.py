"""Day 18 workflow for a repeatable, demo-safe security comparison."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from uuid import uuid4

from ..comparisons.engine import compare_evaluated_records
from ..comparisons.summary import build_comparison_summary
from ..e2e.workflow import run_e2e_workflow
from ..gates.engine import evaluate_security_gate
from ..gates.loader import load_gate_policy
from ..gates.models import GateStatus
from ..loader import load_test_pack
from ..models import ComparisonRecord, ComparisonSummary
from .models import ShowcaseResult


SHOWCASE_ARTIFACT_NAMES = (
    "showcase_summary.md",
    "showcase_manifest.json",
)


def _relative_path(path: Path, parent: Path) -> str:
    return path.relative_to(parent).as_posix()


def _write_summary(
    path: Path,
    *,
    baseline_posture: str,
    candidate_posture: str,
    baseline_findings: int,
    candidate_findings: int,
    summary: ComparisonSummary,
    records: list[ComparisonRecord],
    gate_status: GateStatus,
) -> None:
    lines = [
        "# AI Security Showcase Summary",
        "",
        "## Executive Result",
        "",
        "| Measure | Vulnerable baseline | Hardened candidate |",
        "| --- | ---: | ---: |",
        f"| Observed posture | `{baseline_posture}` | `{candidate_posture}` |",
        f"| Findings | {baseline_findings} | {candidate_findings} |",
        f"| PASS verdicts | {summary.baseline_pass_count} | {summary.candidate_pass_count} |",
        f"| FAIL verdicts | {summary.baseline_fail_count} | {summary.candidate_fail_count} |",
        "",
        "## Test-Level Comparison",
        "",
        "| Test ID | Baseline | Candidate | Outcome |",
        "| --- | --- | --- | --- |",
    ]
    lines.extend(
        "| "
        f"{record.test_id} | {record.baseline_verdict.value} | "
        f"{record.candidate_verdict.value} | {record.outcome.value} |"
        for record in records
    )
    lines.extend(
        [
            "",
            "## Policy Gate",
            "",
            f"Gate status: **{gate_status.value}**",
            "",
            "This result applies only to the included deterministic test pack, "
            "providers, evaluators, and policy. It is not a production-model "
            "security certification.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_manifest(path: Path, payload: dict[str, object]) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_showcase_workflow(
    test_pack_path: Path,
    policy_path: Path,
    *,
    baseline_provider: str = "mock-vulnerable",
    candidate_provider: str = "mock-hardened",
    output_root: Path = Path("output"),
) -> ShowcaseResult:
    """Run two complete assessments and export a safe comparison showcase."""

    if baseline_provider == candidate_provider:
        raise ValueError("Baseline and candidate providers must be different")

    test_pack = load_test_pack(test_pack_path)
    policy = load_gate_policy(policy_path)
    showcase_id = (
        f"SHOWCASE-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
        f"{uuid4().hex[:8]}"
    )
    output_dir = output_root / showcase_id
    output_dir.mkdir(parents=True, exist_ok=False)

    baseline = run_e2e_workflow(
        test_pack_path,
        baseline_provider,
        output_dir / "baseline",
    )
    candidate = run_e2e_workflow(
        test_pack_path,
        candidate_provider,
        output_dir / "candidate",
    )

    comparison_records = compare_evaluated_records(
        test_pack,
        baseline.evaluations,
        candidate.evaluations,
    )
    comparison_summary = build_comparison_summary(test_pack, comparison_records)
    gate_result = evaluate_security_gate(
        policy,
        comparison_summary,
        comparison_records,
    )

    summary_report = output_dir / "showcase_summary.md"
    manifest_report = output_dir / "showcase_manifest.json"
    _write_summary(
        summary_report,
        baseline_posture=baseline.assessment.posture.value,
        candidate_posture=candidate.assessment.posture.value,
        baseline_findings=len(baseline.findings),
        candidate_findings=len(candidate.findings),
        summary=comparison_summary,
        records=comparison_records,
        gate_status=gate_result.gate_status,
    )
    _write_manifest(
        manifest_report,
        {
            "workflow": "day18_showcase_v1",
            "showcase_id": showcase_id,
            "test_pack_name": test_pack.test_pack.name,
            "test_pack_version": test_pack.test_pack.version,
            "completed_stages": [
                "baseline_e2e",
                "candidate_e2e",
                "verdict_comparison",
                "policy_gate",
                "safe_showcase_export",
            ],
            "baseline": {
                "provider": baseline.provider_name,
                "posture": baseline.assessment.posture.value,
                "findings": len(baseline.findings),
                "artifact_directory": _relative_path(
                    baseline.output_dir,
                    output_dir,
                ),
            },
            "candidate": {
                "provider": candidate.provider_name,
                "posture": candidate.assessment.posture.value,
                "findings": len(candidate.findings),
                "artifact_directory": _relative_path(
                    candidate.output_dir,
                    output_dir,
                ),
            },
            "comparison": {
                "total": comparison_summary.total_comparisons,
                "improved": comparison_summary.improved_count,
                "regressed": comparison_summary.regressed_count,
                "unchanged_pass": comparison_summary.unchanged_pass_count,
                "unchanged_issue": comparison_summary.unchanged_issue_count,
                "indeterminate": comparison_summary.indeterminate_count,
            },
            "gate_status": gate_result.gate_status.value,
            "safe_showcase_artifacts": list(SHOWCASE_ARTIFACT_NAMES),
            "raw_prompt_exported": False,
            "raw_response_exported": False,
        },
    )

    return ShowcaseResult(
        showcase_id=showcase_id,
        baseline=baseline,
        candidate=candidate,
        comparison_records=comparison_records,
        comparison_summary=comparison_summary,
        gate_result=gate_result,
        output_dir=output_dir,
        summary_report=summary_report,
        manifest_report=manifest_report,
    )
