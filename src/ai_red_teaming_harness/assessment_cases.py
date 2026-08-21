"""CLI for Day 14 consolidated AI security assessment reporting."""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .assessment.workflow import run_assessment_workflow


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the configured AI red teaming pipeline and export a consolidated assessment report."
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument(
        "--provider",
        required=True,
        help="Provider name, for example mock-vulnerable or mock-hardened",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        report, output_dir = run_assessment_workflow(
            args.path,
            args.provider,
        )
    except Exception as error:  # noqa: BLE001 - CLI boundary
        console.print(f"[bold red]Assessment run failed:[/bold red] {error}")
        raise SystemExit(1) from error

    summary = report.findings_summary

    table = Table(title="AI Security Assessment Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value")

    rows = [
        ("Report ID", report.report_id),
        ("Provider", report.provider_name),
        ("Observed Posture", report.posture.value),
        ("Tests Assessed", str(summary.total_tests_assessed)),
        ("Findings", str(summary.total_findings)),
        ("Critical", str(summary.critical_count)),
        ("High", str(summary.high_count)),
        ("Highest Risk", str(summary.highest_risk_score)),
    ]

    for label, value in rows:
        table.add_row(label, value)

    console.print(table)
    console.print(f"[green]Reports:[/green] {output_dir}")
    console.print(
        "[dim]Posture summarizes only the configured observed assessment scope; "
        "it is not a full security certification.[/dim]"
    )
