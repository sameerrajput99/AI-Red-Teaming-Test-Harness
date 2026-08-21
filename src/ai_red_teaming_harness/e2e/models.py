"""Typed output models for the Day 16 end-to-end workflow."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from ..assessment.models import AssessmentReport
from ..findings.models import FindingsRunSummary, SecurityFinding
from ..models import EvaluatedRecord, ExecutionRecord
from ..risk.models import RiskRecord, RiskRunSummary
from ..stability.models import StabilityRecord, StabilityRunSummary


class E2ERunResult(BaseModel):
    """All stage outputs produced by one complete local assessment run."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    provider_name: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    executions: list[ExecutionRecord]
    evaluations: list[EvaluatedRecord]
    stability_records: list[StabilityRecord]
    stability_summary: StabilityRunSummary
    risk_records: list[RiskRecord]
    risk_summary: RiskRunSummary
    findings: list[SecurityFinding]
    findings_summary: FindingsRunSummary
    assessment: AssessmentReport
    output_dir: Path
    artifact_names: list[str] = Field(min_length=5)
