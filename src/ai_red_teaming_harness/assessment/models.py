"""Typed models for the Day 14 consolidated assessment report."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..findings.models import FindingsRunSummary, SecurityFinding


class AssessmentPosture(str, Enum):
    """Observed assessment posture based on the highest normalized finding."""

    NO_OBSERVED_FINDINGS = "NO_OBSERVED_FINDINGS"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AssessmentReport(BaseModel):
    """Consolidated report built from normalized findings and assessment metadata."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=12, max_length=90)
    title: str = Field(min_length=10, max_length=180)
    provider_name: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    generated_at: datetime
    posture: AssessmentPosture
    executive_summary: str = Field(min_length=20, max_length=2000)
    scope_statement: str = Field(min_length=20, max_length=2000)
    methodology: list[str] = Field(min_length=4, max_length=12)
    findings_summary: FindingsRunSummary
    findings: list[SecurityFinding]
    prioritized_actions: list[str] = Field(max_length=10)
    limitations: list[str] = Field(min_length=3, max_length=10)

    @model_validator(mode="after")
    def validate_findings_count(self) -> "AssessmentReport":
        if len(self.findings) != self.findings_summary.total_findings:
            raise ValueError("findings must match findings_summary.total_findings")
        return self
