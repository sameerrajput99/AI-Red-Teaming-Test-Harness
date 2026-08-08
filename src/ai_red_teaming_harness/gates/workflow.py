"""High-level comparison and security-gate workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..comparisons.workflow import (
    ComparisonArtifacts,
    generate_comparison_artifacts,
)
from ..models import EvaluatedRecord, TestPack
from .engine import evaluate_security_gate
from .models import GatePolicy, GateResult
from .reporter import GateResultWriter


@dataclass(frozen=True)
class GateArtifacts:
    """Comparison artifacts plus the final policy-gate artifact."""

    comparison: ComparisonArtifacts
    gate_report: Path
    gate_result: GateResult


def generate_gate_artifacts(
    test_pack: TestPack,
    baseline_records: list[EvaluatedRecord],
    candidate_records: list[EvaluatedRecord],
    policy: GatePolicy,
    output_root: str | Path = "output",
) -> GateArtifacts:
    """Generate comparison evidence, evaluate policy and persist gate evidence."""

    comparison = generate_comparison_artifacts(
        test_pack,
        baseline_records,
        candidate_records,
        output_root=output_root,
    )
    gate_result = evaluate_security_gate(
        policy,
        comparison.summary,
        comparison.records,
    )
    gate_report = GateResultWriter().write(
        comparison.output_directory / "gate_result.json",
        policy,
        comparison.summary,
        gate_result,
    )
    return GateArtifacts(
        comparison=comparison,
        gate_report=gate_report,
        gate_result=gate_result,
    )
