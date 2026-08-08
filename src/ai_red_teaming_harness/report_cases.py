"Command-line workflow for generating structured AI security evidence files."

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .evaluators.engine import evaluate_test_pack
from .loader import HarnessLoadError, load_test_pack
from .providers.factory import PROVIDER_FACTORIES, get_provider
from .reporters.workflow import ReportArtifacts, generate_report_artifacts
from .runner import run_test_pack

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run, evaluate and export structured AI red teaming evidence."
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument(
        "--provider",
        default="mock-vulnerable",
        choices=sorted(PROVIDER_FACTORIES),
        help="Local chatbot configuration to run and report",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Root directory for generated evidence artifacts",
    )
    return parser


def render_artifacts(artifacts: ReportArtifacts) -> None:
    summary = artifacts.summary
    table = Table(title="Generated Evidence Artifacts")
    table.add_column("Artifact", style="bold")
    table.add_column("Path")
    table.add_row("Full JSON", str(artifacts.json_report))
    table.add_row("Flat CSV", str(artifacts.csv_report))
    table.add_row("Summary JSON", str(artifacts.summary_report))
    table.add_row("HTML Report", str(artifacts.html_report))
    console.print(table)
    console.print(
        "[bold]Run summary:[/bold] "
        f"PASS={summary.pass_count}  "
        f"FAIL={summary.fail_count}  "
        f"REVIEW={summary.review_count}  "
        f"ERROR={summary.error_count}  "
        f"AVG_LATENCY={summary.average_latency_ms} ms"
    )
    console.print(
        "[yellow]Reports contain evidence for the configured tests only; "
        "they are not a full security certification.[/yellow]"
    )


def main() -> None:
    args = build_parser().parse_args()

    try:
        test_pack = load_test_pack(args.path)
        provider = get_provider(args.provider)
        executions = run_test_pack(test_pack, provider)
        evaluated = evaluate_test_pack(test_pack, executions)
        artifacts = generate_report_artifacts(
            test_pack,
            evaluated,
            output_root=args.output_dir,
        )
        render_artifacts(artifacts)
    except (HarnessLoadError, ValueError, OSError) as error:
        console.print(f"[bold red]Reporting error:[/bold red] {error}")
        raise SystemExit(1) from error
    except ValidationError as error:
        console.print("[bold red]Schema validation failed.[/bold red]")
        for item in error.errors():
            location = " -> ".join(str(part) for part in item["loc"])
            console.print(f"  [yellow]{location}[/yellow]: {item['msg']}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
