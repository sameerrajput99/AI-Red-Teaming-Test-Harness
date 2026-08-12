"""JSON/CSV reporters for repeated-run stability results."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import StabilityRecord, StabilityRunSummary


def write_stability_reports(
    output_dir: Path,
    records: list[StabilityRecord],
    summary: StabilityRunSummary,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "stability.json"
    csv_path = output_dir / "stability.csv"
    summary_path = output_dir / "stability_summary.json"

    json_path.write_text(
        json.dumps(
            [record.model_dump(mode="json") for record in records],
            indent=2,
        ),
        encoding="utf-8",
    )

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "test_id",
                "title",
                "category",
                "control_type",
                "severity",
                "total_attempts",
                "pass_count",
                "fail_count",
                "review_count",
                "error_count",
                "pass_rate_percent",
                "verdicts_seen",
                "status",
            ],
        )
        writer.writeheader()
        for record in records:
            data = record.model_dump(mode="json")
            data["verdicts_seen"] = ",".join(data["verdicts_seen"])
            writer.writerow(data)

    summary_path.write_text(
        json.dumps(summary.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )
