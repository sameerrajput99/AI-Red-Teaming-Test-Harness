"""High-level workflow for generating Day 5 comparison artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..models import ComparisonRecord, ComparisonSummary, EvaluatedRecord, TestPack
from .csv_reporter import ComparisonCsvWriter
from .engine import compare_evaluated_records
from .json_reporter import ComparisonJsonWriter
from .summary import build_comparison_summary
from .summary_reporter import ComparisonSummaryWriter


@dataclass(frozen=True)
class ComparisonArtifacts:
    """Paths, records and metrics produced by one comparison workflow."""

    output_directory: Path
    json_report: Path
    csv_report: Path
    summary_report: Path
    records: list[ComparisonRecord]
    summary: ComparisonSummary


def generate_comparison_artifacts(
    test_pack: TestPack,
    baseline_records: list[EvaluatedRecord],
    candidate_records: list[EvaluatedRecord],
    output_root: str | Path = "output",
) -> ComparisonArtifacts:
    """Compare two evaluated runs and persist three side-by-side artifacts."""

    records = compare_evaluated_records(
        test_pack,
        baseline_records,
        candidate_records,
    )
    summary = build_comparison_summary(test_pack, records)
    output_directory = Path(output_root) / summary.comparison_id
    output_directory.mkdir(parents=True, exist_ok=True)

    json_path = ComparisonJsonWriter().write(
        output_directory / "comparison.json",
        test_pack,
        records,
        summary,
    )
    csv_path = ComparisonCsvWriter().write(
        output_directory / "comparison.csv",
        records,
    )
    summary_path = ComparisonSummaryWriter().write(
        output_directory / "comparison_summary.json",
        summary,
    )

    return ComparisonArtifacts(
        output_directory=output_directory,
        json_report=json_path,
        csv_report=csv_path,
        summary_report=summary_path,
        records=records,
        summary=summary,
    )
