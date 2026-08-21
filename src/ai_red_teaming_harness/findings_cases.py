"""CLI for generating normalized security findings from observed AI test risk."""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .findings.workflow import run_findings_workflow


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run AI security tests and generate normalized security findings."
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
        findings, summary, output_dir = run_findings_workflow(
            args.path,
            args.provider,
        )
    except Exception as error:  # noqa: BLE001 - CLI boundary
        console.print(f"[bold red]Findings run failed:[/bold red] {error}")
        raise SystemExit(1) from error

    table = Table(title="Security Findings")
    table.add_column("Finding ID", style="bold")
    table.add_column("Test ID")
    table.add_column("Severity")
    table.add_column("Risk")
    table.add_column("Level")
    table.add_column("Stability")
    table.add_column("Status")

    for finding in findings:
        table.add_row(
            finding.finding_id,
            finding.test_id,
            finding.severity.value,
            str(finding.risk_score),
            finding.risk_level.value,
            finding.stability_status.value,
            finding.status.value,
        )

    console.print(table)
    console.print(
        f"[bold]Summary:[/bold] assessed={summary.total_tests_assessed}, "
        f"findings={summary.total_findings}, "
        f"high_or_critical={summary.high_or_critical_count}, "
        f"highest_risk={summary.highest_risk_score}"
    )
    console.print(f"[green]Artifacts:[/green] {output_dir}")
