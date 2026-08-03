"""JSON writer for complete baseline-versus-candidate comparison evidence."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import ComparisonRecord, ComparisonSummary, TestPack


class ComparisonJsonWriter:
    """Write nested side-by-side evidence to JSON."""

    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[ComparisonRecord],
        summary: ComparisonSummary,
    ) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "1.0",
            "test_pack": test_pack.test_pack.model_dump(mode="json"),
            "summary": summary.model_dump(mode="json"),
            "comparisons": [record.model_dump(mode="json") for record in records],
        }
        destination.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return destination
