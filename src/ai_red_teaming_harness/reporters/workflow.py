"High-level workflow for generating all run report artifacts."

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..models import EvaluatedRecord, RunSummary, TestPack
from .csv_reporter import CsvReportWriter
from .html_reporter import HtmlReportWriter
from .json_reporter import JsonReportWriter
from .summary import build_run_summary
from .summary_reporter import SummaryReportWriter


@dataclass(frozen=True)
class ReportArtifacts:
    """Paths and summary produced by one reporting workflow."""

    output_directory: Path
    json_report: Path
    csv_report: Path
    summary_report: Path
    html_report: Path
    summary: RunSummary


def generate_report_artifacts(
    test_pack: TestPack,
    records: list[EvaluatedRecord],
    output_root: str | Path = "output",
) -> ReportArtifacts:
    """Write JSON, CSV, summary and HTML files into one run directory."""

    summary = build_run_summary(test_pack, records)
    output_directory = Path(output_root) / summary.run_id
    output_directory.mkdir(parents=True, exist_ok=True)

    json_path = JsonReportWriter().write(
        output_directory / "results.json",
        test_pack,
        records,
        summary,
    )
    csv_path = CsvReportWriter().write(
        output_directory / "results.csv",
        test_pack,
        records,
        summary,
    )
    summary_path = SummaryReportWriter().write(
        output_directory / "summary.json",
        test_pack,
        records,
        summary,
    )
    html_path = HtmlReportWriter().write(
        output_directory / "results.html",
        test_pack,
        records,
        summary,
    )

    return ReportArtifacts(
        output_directory=output_directory,
        json_report=json_path,
        csv_report=csv_path,
        summary_report=summary_path,
        html_report=html_path,
        summary=summary,
    )
