"""Secret-safe provider configuration inspection without a network request."""

from __future__ import annotations

import argparse

from rich.console import Console
from rich.table import Table

from .provider_config import inspect_openai_environment
from .providers.factory import PROVIDER_FACTORIES


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Inspect provider configuration without sending a network request."
    )
    parser.add_argument(
        "--provider",
        choices=sorted(PROVIDER_FACTORIES),
        default="openai-live",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.provider != "openai-live":
        console.print(
            f"[green]{args.provider}[/green] is local and requires no secret."
        )
        console.print("[bold]Network request:[/bold] NOT SENT")
        return

    summary = inspect_openai_environment()
    table = Table(title="Secret-Safe Provider Configuration")
    table.add_column("Setting", style="bold")
    table.add_column("Value")
    table.add_row("Provider", str(summary["provider"]))
    table.add_row(
        "API key configured",
        "yes" if summary["api_key_configured"] else "no",
    )
    table.add_row("Model", str(summary["model"]))
    table.add_row("Base URL", str(summary["base_url"]))
    table.add_row("Timeout", f'{summary["timeout_seconds"]} seconds')
    table.add_row("Max retries", str(summary["max_retries"]))
    table.add_row("Network request", "NOT SENT")
    console.print(table)

    if not summary["api_key_configured"] or summary["model"] == "<missing>":
        console.print(
            "[yellow]openai-live is not fully configured. "
            "Copy .env.example to .env and fill required values locally.[/yellow]"
        )
    else:
        console.print(
            "[green]openai-live configuration appears ready for an optional live call.[/green]"
        )


if __name__ == "__main__":
    main()
