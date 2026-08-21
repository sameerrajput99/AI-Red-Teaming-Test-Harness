"""CLI for Day 16 integration and end-to-end verification."""

from __future__ import annotations

import argparse
from pathlib import Path

from rich.console import Console
from rich.table import Table

from .e2e.workflow import run_e2e_workflow


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run the complete AI red teaming pipeline and verify its safe "
            "end-to-end artifacts."
        )
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument("--provider", required=True, help="Local provider name")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    try:
        result = run_e2e_workflow(args.path, args.provider)
    except Exception as error:  # noqa: BLE001 - CLI boundary
        console.print(f"[bold red]End-to-end run failed:[/bold red] {error}")
        raise SystemExit(1) from error

    table = Table(title="Day 16 End-to-End Verification")
    table.add_column("Stage", style="bold")
    table.add_column("Result")
    rows = [
        ("Provider", result.provider_name),
        ("Executions", str(len(result.executions))),
        ("Evaluations", str(len(result.evaluations))),
        ("Stability Records", str(len(result.stability_records))),
        ("Risk Records", str(len(result.risk_records))),
        ("Findings", str(len(result.findings))),
        ("Observed Posture", result.assessment.posture.value),
        ("Artifacts", str(len(result.artifact_names))),
    ]
    for label, value in rows:
        table.add_row(label, value)

    console.print(table)
    console.print(f"[green]Verified artifacts:[/green] {result.output_dir}")
    console.print(
        "[dim]This verifies the configured observed workflow; it is not a "
        "complete security certification.[/dim]"
    )
