"""Compact JSON writer for comparison-level metrics."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import ComparisonSummary


class ComparisonSummaryWriter:
    """Write compact comparison metrics without full raw responses."""

    def write(self, destination: Path, summary: ComparisonSummary) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(summary.model_dump(mode="json"), indent=2),
            encoding="utf-8",
        )
        return destination
