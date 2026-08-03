"""CSV reporter that flattens evaluated records for tabular analysis."""

from __future__ import annotations

import csv
from pathlib import Path

from ..models import EvaluatedRecord, RunSummary, TestPack
from .base import ReportWriter


CSV_FIELDS = [
    "run_id",
    "test_id",
    "title",
    "category",
    "control_type",
    "severity",
    "expected_behavior",
    "provider_name",
    "execution_status",
    "security_verdict",
    "latency_ms",
    "timestamp",
    "prompt",
    "response",
    "error_message",
    "evaluation_summary",
    "evaluator_types",
    "finding_verdicts",
    "matched_values",
    "finding_reasons",
]


class CsvReportWriter(ReportWriter):
    """Write one flattened row per evaluated execution."""

    @property
    def format_name(self) -> str:
        return "csv"

    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[EvaluatedRecord],
        summary: RunSummary,
    ) -> Path:
        del summary  # CSV rows already contain run-level identifiers.
        destination.parent.mkdir(parents=True, exist_ok=True)
        cases_by_id = {case.id: case for case in test_pack.test_cases}

        with destination.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()

            for record in records:
                execution = record.execution
                test_case = cases_by_id.get(execution.test_id)
                if test_case is None:
                    raise ValueError(
                        f"No test definition was found for {execution.test_id}"
                    )

                matched_values = sorted(
                    {
                        value
                        for finding in record.findings
                        for value in finding.matched_values
                    }
                )
                writer.writerow(
                    {
                        "run_id": execution.run_id,
                        "test_id": execution.test_id,
                        "title": test_case.title,
                        "category": test_case.category.value,
                        "control_type": test_case.control_type.value,
                        "severity": test_case.severity.value,
                        "expected_behavior": test_case.expected_behavior,
                        "provider_name": execution.provider_name,
                        "execution_status": execution.execution_status.value,
                        "security_verdict": record.security_verdict.value,
                        "latency_ms": execution.latency_ms,
                        "timestamp": execution.timestamp.isoformat(),
                        "prompt": execution.prompt,
                        "response": execution.response or "",
                        "error_message": execution.error_message or "",
                        "evaluation_summary": record.summary,
                        "evaluator_types": " | ".join(
                            finding.evaluator_type for finding in record.findings
                        ),
                        "finding_verdicts": " | ".join(
                            finding.verdict.value for finding in record.findings
                        ),
                        "matched_values": " | ".join(matched_values),
                        "finding_reasons": " || ".join(
                            finding.reason for finding in record.findings
                        ),
                    }
                )

        return destination
