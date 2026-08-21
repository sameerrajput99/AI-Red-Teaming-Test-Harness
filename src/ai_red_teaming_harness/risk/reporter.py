"""JSON/CSV reporters for Day 12 risk scoring."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import RiskRecord, RiskRunSummary


def write_risk_reports(
    output_dir: Path,
    records: list[RiskRecord],
    summary: RiskRunSummary,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "risk.json").write_text(
        json.dumps([record.model_dump(mode="json") for record in records], indent=2),
        encoding="utf-8",
    )

    with (output_dir / "risk.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "test_id",
                "title",
                "category",
                "control_type",
                "severity",
                "stability_status",
                "total_attempts",
                "pass_rate_percent",
                "observed_issue_factor_percent",
                "severity_score",
                "instability_uplift",
                "risk_score",
                "risk_level",
                "rationale",
            ],
        )
        writer.writeheader()
        for record in records:
            writer.writerow(record.model_dump(mode="json"))

    (output_dir / "risk_summary.json").write_text(
        json.dumps(summary.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )
