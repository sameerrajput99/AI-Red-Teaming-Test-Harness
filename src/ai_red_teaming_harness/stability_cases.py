"""CLI for repeated-run stability and flakiness analysis."""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .stability.workflow import run_stability_workflow


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run repeated AI security tests and analyze pass rate and flakiness."
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument(
        "--provider",
        required=True,
        help="Provider name, for example mock-hardened or mock-flaky",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        records, summary, output_dir = run_stability_workflow(
            args.path,
            args.provider,
        )
    except Exception as error:  # noqa: BLE001 - CLI boundary
        console.print(f"[bold red]Stability run failed:[/bold red] {error}")
        raise SystemExit(1) from error

    table = Table(title="Repeated-Run Stability Analysis")
    table.add_column("Test ID", style="bold")
    table.add_column("Attempts")
    table.add_column("PASS")
    table.add_column("FAIL")
    table.add_column("REVIEW")
    table.add_column("ERROR")
    table.add_column("Pass Rate")
    table.add_column("Status")

    for record in records:
        table.add_row(
            record.test_id,
            str(record.total_attempts),
            str(record.pass_count),
            str(record.fail_count),
            str(record.review_count),
            str(record.error_count),
            f"{record.pass_rate_percent:.1f}%",
            record.status.value,
        )

    console.print(table)
    console.print(
        f"[bold]Summary:[/bold] tests={summary.total_tests}, "
        f"attempts={summary.total_attempts}, "
        f"stable_pass={summary.stable_pass_count}, "
        f"stable_issue={summary.stable_issue_count}, "
        f"flaky={summary.flaky_count}, "
        f"avg_pass_rate={summary.average_pass_rate_percent:.1f}%"
    )
    console.print(f"[green]Artifacts:[/green] {output_dir}")
