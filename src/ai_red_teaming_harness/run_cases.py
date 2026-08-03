"""Command-line runner for executing validated AI red teaming test packs."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .loader import HarnessLoadError, load_test_pack
from .models import ExecutionRecord
from .providers.factory import PROVIDER_FACTORIES, get_provider
from .runner import run_test_pack

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a validated AI red teaming test pack against a local provider."
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument(
        "--provider",
        default="mock-vulnerable",
        choices=sorted(PROVIDER_FACTORIES),
        help="Local chatbot configuration to execute",
    )
    return parser


def shorten(value: str | None, limit: int = 78) -> str:
    if value is None:
        return "-"
    one_line = " ".join(value.split())
    return one_line if len(one_line) <= limit else f"{one_line[: limit - 3]}..."


def render_records(records: list[ExecutionRecord]) -> None:
    table = Table(title="Raw Test Execution Evidence")
    table.add_column("Test ID", style="bold")
    table.add_column("Provider")
    table.add_column("Status")
    table.add_column("Latency")
    table.add_column("Raw response / error")

    for record in records:
        evidence = record.response or record.error_message
        table.add_row(
            record.test_id,
            record.provider_name,
            record.execution_status.value,
            f"{record.latency_ms} ms",
            shorten(evidence),
        )

    console.print(table)
    success_count = sum(record.execution_status.value == "success" for record in records)
    error_count = len(records) - success_count
    console.print(
        f"[bold green]Executed {len(records)} cases:[/bold green] "
        f"{success_count} success, {error_count} error."
    )
    console.print(
        "[yellow]No PASS/FAIL security verdicts yet. Day 2 captures raw execution evidence only.[/yellow]"
    )


def main() -> None:
    args = build_parser().parse_args()

    try:
        test_pack = load_test_pack(args.path)
        provider = get_provider(args.provider)
        records = run_test_pack(test_pack, provider)
        render_records(records)
    except (HarnessLoadError, ValueError) as error:
        console.print(f"[bold red]Execution setup error:[/bold red] {error}")
        raise SystemExit(1) from error
    except ValidationError as error:
        console.print("[bold red]Schema validation failed.[/bold red]")
        for item in error.errors():
            location = " -> ".join(str(part) for part in item["loc"])
            console.print(f"  [yellow]{location}[/yellow]: {item['msg']}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
