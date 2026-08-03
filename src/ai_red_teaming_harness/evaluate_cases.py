"""Command-line workflow for executing and evaluating AI red teaming tests."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .evaluators.engine import evaluate_test_pack
from .loader import HarnessLoadError, load_test_pack
from .models import EvaluatedRecord, EvaluationVerdict
from .providers.factory import PROVIDER_FACTORIES, get_provider
from .runner import run_test_pack

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run and evaluate a validated AI red teaming test pack."
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument(
        "--provider",
        default="mock-vulnerable",
        choices=sorted(PROVIDER_FACTORIES),
        help="Local chatbot configuration to execute and evaluate",
    )
    return parser


def shorten(value: str, limit: int = 72) -> str:
    one_line = " ".join(value.split())
    return one_line if len(one_line) <= limit else f"{one_line[: limit - 3]}..."


def verdict_style(verdict: EvaluationVerdict) -> str:
    return {
        EvaluationVerdict.PASS: "bold green",
        EvaluationVerdict.FAIL: "bold red",
        EvaluationVerdict.REVIEW: "bold yellow",
        EvaluationVerdict.ERROR: "bold magenta",
    }[verdict]


def render_results(records: list[EvaluatedRecord]) -> None:
    table = Table(title="Security Evaluation Results")
    table.add_column("Test ID", style="bold")
    table.add_column("Provider")
    table.add_column("Execution")
    table.add_column("Verdict")
    table.add_column("Evaluation summary")

    for record in records:
        execution = record.execution
        table.add_row(
            execution.test_id,
            execution.provider_name,
            execution.execution_status.value,
            f"[{verdict_style(record.security_verdict)}]{record.security_verdict.value}[/]",
            shorten(record.summary),
        )

    console.print(table)
    counts = Counter(record.security_verdict.value for record in records)
    console.print(
        "[bold]Summary:[/bold] "
        f"PASS={counts['PASS']}  "
        f"FAIL={counts['FAIL']}  "
        f"REVIEW={counts['REVIEW']}  "
        f"ERROR={counts['ERROR']}"
    )
    console.print(
        "[yellow]These verdicts apply only to the configured test cases and evaluators; "
        "they do not prove that a model is fully secure.[/yellow]"
    )


def main() -> None:
    args = build_parser().parse_args()

    try:
        test_pack = load_test_pack(args.path)
        provider = get_provider(args.provider)
        executions = run_test_pack(test_pack, provider)
        evaluated = evaluate_test_pack(test_pack, executions)
        render_results(evaluated)
    except (HarnessLoadError, ValueError) as error:
        console.print(f"[bold red]Evaluation setup error:[/bold red] {error}")
        raise SystemExit(1) from error
    except ValidationError as error:
        console.print("[bold red]Schema validation failed.[/bold red]")
        for item in error.errors():
            location = " -> ".join(str(part) for part in item["loc"])
            console.print(f"  [yellow]{location}[/yellow]: {item['msg']}")
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()
