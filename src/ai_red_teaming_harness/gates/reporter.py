"""JSON writer for policy-gate evidence."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import ComparisonSummary
from .models import GatePolicy, GateResult


class GateResultWriter:
    """Persist policy, comparison metrics and rule-level decisions."""

    def write(
        self,
        destination: Path,
        policy: GatePolicy,
        comparison_summary: ComparisonSummary,
        gate_result: GateResult,
    ) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema_version": "1.0",
            "policy": policy.model_dump(mode="json"),
            "comparison_summary": comparison_summary.model_dump(mode="json"),
            "gate_result": gate_result.model_dump(mode="json"),
        }
        destination.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        return destination
