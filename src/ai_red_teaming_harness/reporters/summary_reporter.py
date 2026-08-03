"""Compact JSON writer for run-level metrics."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import EvaluatedRecord, RunSummary, TestPack
from .base import ReportWriter


class SummaryReportWriter(ReportWriter):
    """Write a compact run summary without full prompts and responses."""

    @property
    def format_name(self) -> str:
        return "summary-json"

    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[EvaluatedRecord],
        summary: RunSummary,
    ) -> Path:
        del test_pack, records
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(summary.model_dump(mode="json"), indent=2),
            encoding="utf-8",
        )
        return destination
