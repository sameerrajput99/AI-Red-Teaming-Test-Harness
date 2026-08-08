"""Command-line policy gate for baseline-versus-candidate security evidence."""

from __future__ import annotations

import argparse
from pathlib import Path

from pydantic import ValidationError
from rich.console import Console
from rich.table import Table

from .evaluators.engine import evaluate_test_pack
from .gates.loader import GatePolicyLoadError, load_gate_policy
from .gates.models import GateStatus
from .gates.workflow import GateArtifacts, generate_gate_artifacts
from .loader import HarnessLoadError, load_test_pack
from .providers.factory import PROVIDER_FACTORIES, get_provider
from .runner import run_test_pack


console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run baseline and candidate configurations, compare their verdicts, "
            "and enforce a YAML security policy."
        )
    )
    parser.add_argument("path", type=Path, help="Path to the YAML test pack")
    parser.add_argument(
        "--policy",
        type=Path,
        default=Path("policies/strict_gate.yaml"),
        help="Path to the YAML security-gate policy",
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
        help="Root directory for generated artifacts",
    )
    return parser


def render_gate(artifacts: GateArtifacts) -> None:
    result = artifacts.gate_result
    status_style = "bold green" if result.gate_status is GateStatus.PASSED else "bold red"

    table = Table(title="AI Security Policy Gate")
    table.add_column("Rule", style="bold")
    table.add_column("Observed")
    table.add_column("Expected")
    table.add_column("Result")

    for rule in result.rule_results:
        outcome = "PASS" if rule.passed else "FAIL"
        style = "green" if rule.passed else "red"
        table.add_row(
            rule.rule_id,
            str(rule.observed),
            rule.expected,
            f"[{style}]{outcome}[/]",
        )

    console.print(table)
    console.print(
        f"[bold]Policy:[/bold] {result.policy_name} v{result.policy_version}"
    )
    console.print(
        f"[bold]Gate status:[/bold] [{status_style}]{result.gate_status.value}[/]"
    )
    console.print(f"[bold]Gate evidence:[/bold] {artifacts.gate_report}")
    console.print(
        "[yellow]A passed gate applies only to the configured policy, "
        "test pack and evaluators.[/yellow]"
    )


def main() -> None:
    args = build_parser().parse_args()

    try:
        if args.baseline == args.candidate:
            raise ValueError("Baseline and candidate providers must be different")

        test_pack = load_test_pack(args.path)
        policy = load_gate_policy(args.policy)

        baseline_executions = run_test_pack(
            test_pack,
            get_provider(args.baseline),
        )
        candidate_executions = run_test_pack(
            test_pack,
            get_provider(args.candidate),
        )
        baseline_records = evaluate_test_pack(test_pack, baseline_executions)
        candidate_records = evaluate_test_pack(test_pack, candidate_executions)

        artifacts = generate_gate_artifacts(
            test_pack,
            baseline_records,
            candidate_records,
            policy,
            output_root=args.output_dir,
        )
        render_gate(artifacts)

        if artifacts.gate_result.gate_status is GateStatus.FAILED:
            raise SystemExit(1)

    except SystemExit:
        raise
    except (
        GatePolicyLoadError,
        HarnessLoadError,
        ValueError,
        OSError,
        ValidationError,
    ) as error:
        console.print(f"[bold red]Gate error:[/bold red] {error}")
        raise SystemExit(2) from error


if __name__ == "__main__":
    main()
