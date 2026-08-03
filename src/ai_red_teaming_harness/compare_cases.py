"""Command-line baseline-versus-candidate security comparison."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .comparisons.workflow import ComparisonArtifacts, generate_comparison_artifacts
from .evaluators.engine import evaluate_test_pack
from .loader import HarnessLoadError, load_test_pack
from .providers.factory import PROVIDER_FACTORIES, get_provider
from .runner import run_test_pack


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run one test pack against a baseline and candidate provider, "
            "then generate side-by-side security comparison evidence."
        )
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
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
        help="Root directory for generated comparison artifacts",
    )
    return parser


def render_comparison(artifacts: ComparisonArtifacts) -> None:
    summary = artifacts.summary
    table = Table(title="Baseline vs Candidate Security Comparison")
    table.add_column("Test ID", style="bold")
    table.add_column("Attempt")
    table.add_column(f"Baseline ({summary.baseline_provider})")
    table.add_column(f"Candidate ({summary.candidate_provider})")
    table.add_column("Outcome")

    outcome_styles = {
        "IMPROVED": "bold green",
        "REGRESSED": "bold red",
        "UNCHANGED_PASS": "green",
        "UNCHANGED_ISSUE": "yellow",
        "INDETERMINATE": "magenta",
    }
    for record in artifacts.records:
        table.add_row(
            record.test_id,
            str(record.attempt),
            record.baseline_verdict.value,
            record.candidate_verdict.value,
            f"[{outcome_styles[record.outcome.value]}]{record.outcome.value}[/]",
        )

    console.print(table)
    console.print(
        "[bold]Comparison summary:[/bold] "
        f"IMPROVED={summary.improved_count}  "
        f"REGRESSED={summary.regressed_count}  "
        f"UNCHANGED_PASS={summary.unchanged_pass_count}  "
        f"UNCHANGED_ISSUE={summary.unchanged_issue_count}  "
        f"INDETERMINATE={summary.indeterminate_count}"
    )

    files = Table(title="Generated Comparison Artifacts")
    files.add_column("Artifact", style="bold")
    files.add_column("Path")
    files.add_row("Comparison JSON", str(artifacts.json_report))
    files.add_row("Comparison CSV", str(artifacts.csv_report))
    files.add_row("Comparison Summary", str(artifacts.summary_report))
    console.print(files)
    console.print(
        "[yellow]An improved result applies only to the configured test pack and "
        "evaluators; it is not a complete security certification.[/yellow]"
    )


def main() -> None:
    args = build_parser().parse_args()

    try:
        if args.baseline == args.candidate:
            raise ValueError("Baseline and candidate providers must be different")

        test_pack = load_test_pack(args.path)
        baseline_executions = run_test_pack(test_pack, get_provider(args.baseline))
        candidate_executions = run_test_pack(test_pack, get_provider(args.candidate))
        baseline_records = evaluate_test_pack(test_pack, baseline_executions)
        candidate_records = evaluate_test_pack(test_pack, candidate_executions)
        artifacts = generate_comparison_artifacts(
            test_pack,
            baseline_records,
            candidate_records,
            output_root=args.output_dir,
        )
        render_comparison(artifacts)
    except (HarnessLoadError, ValueError, OSError) as error:
        console.print(f"[bold red]Comparison error:[/bold red] {error}")
        raise SystemExit(1) from error
    except ValidationError as error:
        console.print("[bold red]Schema validation failed.[/bold red]")
        for item in error.errors():
            location = " -> ".join(str(part) for part in item["loc"])
            console.print(f"  [yellow]{location}[/yellow]: {item['msg']}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
