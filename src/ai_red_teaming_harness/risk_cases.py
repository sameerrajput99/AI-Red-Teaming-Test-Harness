"""CLI for deterministic Day 12 AI security risk scoring."""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .risk.workflow import run_risk_workflow


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run repeated AI security tests and calculate prioritization risk scores."
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
        records, summary, output_dir = run_risk_workflow(args.path, args.provider)
    except Exception as error:  # noqa: BLE001 - CLI boundary
        console.print(f"[bold red]Risk run failed:[/bold red] {error}")
        raise SystemExit(1) from error

    table = Table(title="AI Security Risk Prioritization")
    table.add_column("Test ID", style="bold")
    table.add_column("Severity")
    table.add_column("Attempts")
    table.add_column("Pass Rate")
    table.add_column("Stability")
    table.add_column("Risk Score")
    table.add_column("Risk Level")

    for record in records:
        table.add_row(
            record.test_id,
            record.severity.value.upper(),
            str(record.total_attempts),
            f"{record.pass_rate_percent:.1f}%",
            record.stability_status.value,
            str(record.risk_score),
            record.risk_level.value,
        )

    console.print(table)
    console.print(
        f"[bold]Summary:[/bold] tests={summary.total_tests}, "
        f"none={summary.none_count}, low={summary.low_count}, "
        f"medium={summary.medium_count}, high={summary.high_count}, "
        f"critical={summary.critical_count}, "
        f"highest={summary.highest_risk_score}, "
        f"average={summary.average_risk_score:.1f}"
    )
    console.print(f"[green]Artifacts:[/green] {output_dir}")
    console.print(
        "[yellow]Note:[/yellow] This is a project-specific prioritization heuristic, "
        "not CVSS and not a security certification."
    )
