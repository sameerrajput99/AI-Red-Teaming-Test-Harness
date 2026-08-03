"""JSON reporter that preserves nested findings and raw evidence."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import EvaluatedRecord, RunSummary, TestPack
from .base import ReportWriter


class JsonReportWriter(ReportWriter):
    """Write a complete machine-readable JSON evidence report."""

    @property
    def format_name(self) -> str:
        return "json"

    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[EvaluatedRecord],
        summary: RunSummary,
    ) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "1.0",
            "test_pack": test_pack.test_pack.model_dump(mode="json"),
            "summary": summary.model_dump(mode="json"),
            "results": [record.model_dump(mode="json") for record in records],
        }
        destination.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return destination
