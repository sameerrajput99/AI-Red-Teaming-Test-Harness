"""Typed Day 13 security finding models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..models import Category, ControlType, Severity
from ..risk.models import RiskLevel
from ..stability.models import StabilityStatus


class FindingStatus(str, Enum):
    """Simple initial lifecycle state for an observed security finding."""

    OPEN = "OPEN"


class SecurityFinding(BaseModel):
    """Normalized security issue derived from observed risk evidence."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=9, max_length=40)
    test_id: str = Field(min_length=5, max_length=30)
    title: str = Field(min_length=5, max_length=160)
    provider_name: str = Field(min_length=2, max_length=100)
    category: Category
    control_type: ControlType
    severity: Severity
    risk_score: int = Field(ge=1, le=100)
    risk_level: RiskLevel
    stability_status: StabilityStatus
    pass_rate_percent: float = Field(ge=0, le=100)
    observed_issue_factor_percent: float = Field(gt=0, le=100)
    status: FindingStatus = FindingStatus.OPEN
    observation: str = Field(min_length=10, max_length=1000)
    impact: str = Field(min_length=10, max_length=1000)
    recommendation: str = Field(min_length=10, max_length=1200)
    evidence_summary: str = Field(min_length=10, max_length=1000)
    created_at: datetime


class FindingsRunSummary(BaseModel):
    """Run-level summary for normalized security findings."""

    model_config = ConfigDict(extra="forbid")

    provider_name: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    total_tests_assessed: int = Field(ge=1)
    total_findings: int = Field(ge=0)
    low_count: int = Field(ge=0)
    medium_count: int = Field(ge=0)
    high_count: int = Field(ge=0)
    critical_count: int = Field(ge=0)
    high_or_critical_count: int = Field(ge=0)
    highest_risk_score: int = Field(ge=0, le=100)
    generated_at: datetime

    @model_validator(mode="after")
    def validate_counts(self) -> "FindingsRunSummary":
        counted = (
            self.low_count
            + self.medium_count
            + self.high_count
            + self.critical_count
        )
        if counted != self.total_findings:
            raise ValueError("finding level counts must equal total_findings")
        if self.high_or_critical_count != self.high_count + self.critical_count:
            raise ValueError("high_or_critical_count must equal high_count + critical_count")
        return self
