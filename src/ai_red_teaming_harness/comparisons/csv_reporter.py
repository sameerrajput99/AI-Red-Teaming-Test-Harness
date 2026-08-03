"""CSV writer for analyst-friendly side-by-side comparison rows."""

from __future__ import annotations

import csv
from pathlib import Path

from ..models import ComparisonRecord


CSV_FIELDS = [
    "test_id",
    "attempt",
    "title",
    "category",
    "control_type",
    "severity",
    "baseline_provider",
    "baseline_run_id",
    "baseline_verdict",
    "baseline_response",
    "candidate_provider",
    "candidate_run_id",
    "candidate_verdict",
    "candidate_response",
    "outcome",
    "explanation",
]


class ComparisonCsvWriter:
    """Write one flat row per aligned test attempt."""

    def write(self, destination: Path, records: list[ComparisonRecord]) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for record in records:
                writer.writerow(
                    {
                        "test_id": record.test_id,
                        "attempt": record.attempt,
                        "title": record.title,
                        "category": record.category.value,
                        "control_type": record.control_type.value,
                        "severity": record.severity.value,
                        "baseline_provider": record.baseline_provider,
                        "baseline_run_id": record.baseline_run_id,
                        "baseline_verdict": record.baseline_verdict.value,
                        "baseline_response": record.baseline_response or "",
                        "candidate_provider": record.candidate_provider,
                        "candidate_run_id": record.candidate_run_id,
                        "candidate_verdict": record.candidate_verdict.value,
                        "candidate_response": record.candidate_response or "",
                        "outcome": record.outcome.value,
                        "explanation": record.explanation,
                    }
                )
        return destination
