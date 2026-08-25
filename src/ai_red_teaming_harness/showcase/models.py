"""Typed result returned by the Day 18 showcase workflow."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from ..e2e.models import E2ERunResult
from ..gates.models import GateResult
from ..models import ComparisonRecord, ComparisonSummary


class ShowcaseResult(BaseModel):
    """In-memory evidence and safe artifact paths for one showcase run."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    showcase_id: str
    baseline: E2ERunResult
    candidate: E2ERunResult
    comparison_records: list[ComparisonRecord]
    comparison_summary: ComparisonSummary
    gate_result: GateResult
    output_dir: Path
    summary_report: Path
    manifest_report: Path
