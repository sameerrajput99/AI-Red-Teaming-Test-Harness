"""Command-line Day 18 vulnerable-versus-hardened showcase."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .gates.loader import GatePolicyLoadError
from .gates.models import GateStatus
from .loader import HarnessLoadError
from .providers.factory import PROVIDER_FACTORIES
from .showcase.models import ShowcaseResult
from .showcase.workflow import run_showcase_workflow


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run a repeatable vulnerable-versus-hardened AI security showcase "
            "and export safe summary evidence."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path("test_packs/day18_showcase_pack.yaml"),
        help="Path to the showcase YAML test pack",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("policies/strict_gate.yaml"),
        help="Path to the security-gate policy",
    )
    parser.add_argument(
        "--baseline",
        choices=sorted(PROVIDER_FACTORIES),
        default="mock-vulnerable",
        help="Reference provider configuration",
    )
    parser.add_argument(
        "--candidate",
        choices=sorted(PROVIDER_FACTORIES),
        default="mock-hardened",
        help="Candidate provider configuration",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Root directory for generated showcase artifacts",
    )
    return parser


def render_showcase(result: ShowcaseResult) -> None:
    comparison = Table(title="Day 18 AI Security Showcase")
    comparison.add_column("Test ID", style="bold")
    comparison.add_column(f"Baseline ({result.baseline.provider_name})")
    comparison.add_column(f"Candidate ({result.candidate.provider_name})")
    comparison.add_column("Outcome")

    for record in result.comparison_records:
        outcome_style = "green" if record.outcome.value == "IMPROVED" else "cyan"
        comparison.add_row(
            record.test_id,
            record.baseline_verdict.value,
            record.candidate_verdict.value,
            f"[{outcome_style}]{record.outcome.value}[/]",
        )
    console.print(comparison)

    result_table = Table(title="Showcase Result")
    result_table.add_column("Measure", style="bold")
    result_table.add_column("Observed")
    result_table.add_row(
        "Baseline posture",
        result.baseline.assessment.posture.value,
    )
    result_table.add_row(
        "Candidate posture",
        result.candidate.assessment.posture.value,
    )
    result_table.add_row(
        "Improvements",
        str(result.comparison_summary.improved_count),
    )
    result_table.add_row(
        "Regressions",
        str(result.comparison_summary.regressed_count),
    )
    result_table.add_row("Policy gate", result.gate_result.gate_status.value)
    console.print(result_table)
    console.print(f"[bold]Safe summary:[/bold] {result.summary_report}")
    console.print(f"[bold]Showcase manifest:[/bold] {result.manifest_report}")
    console.print(
        "[yellow]This deterministic showcase is scoped evidence, not a "
        "production-model security certification.[/yellow]"
    )


def main() -> None:
    args = build_parser().parse_args()
    try:
        result = run_showcase_workflow(
            args.path,
            args.policy,
            baseline_provider=args.baseline,
            candidate_provider=args.candidate,
            output_root=args.output_dir,
        )
        render_showcase(result)
        if result.gate_result.gate_status is GateStatus.FAILED:
            raise SystemExit(1)
    except SystemExit:
        raise
    except (
        GatePolicyLoadError,
        HarnessLoadError,
        OSError,
        ValidationError,
        ValueError,
    ) as error:
        console.print(f"[bold red]Showcase failed:[/bold red] {error}")
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
