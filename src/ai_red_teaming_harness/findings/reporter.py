"""Structured JSON and CSV exports for Day 13 security findings."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from .models import FindingsRunSummary, SecurityFinding


def write_findings_reports(
    output_dir: Path,
    findings: list[SecurityFinding],
    summary: FindingsRunSummary,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "findings.json"
    csv_path = output_dir / "findings.csv"
    summary_path = output_dir / "findings_summary.json"

    json_path.write_text(
        json.dumps(
            [finding.model_dump(mode="json") for finding in findings],
            indent=2,
        ),
        encoding="utf-8",
    )

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "finding_id",
            "test_id",
            "title",
            "provider_name",
            "category",
            "control_type",
            "severity",
            "risk_score",
            "risk_level",
            "stability_status",
            "pass_rate_percent",
            "observed_issue_factor_percent",
            "status",
            "observation",
            "impact",
            "recommendation",
            "evidence_summary",
            "created_at",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for finding in findings:
            writer.writerow(finding.model_dump(mode="json"))

    summary_path.write_text(
        json.dumps(summary.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )
