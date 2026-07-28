"""Command-line validator for YAML AI red teaming test packs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .loader import HarnessLoadError, load_test_pack

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate an AI red teaming YAML test pack."
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    return parser


def render_success(path: Path) -> None:
    pack = load_test_pack(path)

    table = Table(title=f"Validated: {pack.test_pack.name}")
    table.add_column("ID", style="bold")
    table.add_column("Category")
    table.add_column("Type")
    table.add_column("Severity")
    table.add_column("Expected behavior")

    for case in pack.test_cases:
        table.add_row(
            case.id,
            case.category.value,
            case.control_type.value,
            case.severity.value,
            case.expected_behavior,
        )

    console.print(table)
    console.print(
        f"[bold green]Validated {len(pack.test_cases)} test cases successfully.[/bold green]"
    )


def main() -> None:
    args = build_parser().parse_args()

    try:
        render_success(args.path)
    except HarnessLoadError as error:
        console.print(f"[bold red]Load error:[/bold red] {error}")
        raise SystemExit(1) from error
    except ValidationError as error:
        console.print("[bold red]Schema validation failed.[/bold red]")
        for item in error.errors():
            location = " -> ".join(str(part) for part in item["loc"])
            console.print(f"  [yellow]{location}[/yellow]: {item['msg']}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
