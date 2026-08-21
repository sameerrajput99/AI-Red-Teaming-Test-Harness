"""Typed models for Day 12 risk scoring."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..models import Category, ControlType, Severity
from ..stability.models import StabilityStatus


class RiskLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskRecord(BaseModel):
    """Risk-prioritization result for one stability record."""

    model_config = ConfigDict(extra="forbid")

    test_id: str = Field(min_length=5, max_length=30)
    title: str = Field(min_length=5, max_length=140)
    category: Category
    control_type: ControlType
    severity: Severity
    stability_status: StabilityStatus
    total_attempts: int = Field(ge=1)
    pass_rate_percent: float = Field(ge=0, le=100)
    observed_issue_factor_percent: float = Field(ge=0, le=100)
    severity_score: int = Field(ge=0, le=100)
    instability_uplift: float = Field(ge=0, le=20)
    risk_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    rationale: str = Field(min_length=10, max_length=1000)


class RiskRunSummary(BaseModel):
    """Run-level risk-prioritization summary."""

    model_config = ConfigDict(extra="forbid")

    provider_name: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    total_tests: int = Field(ge=1)
    none_count: int = Field(ge=0)
    low_count: int = Field(ge=0)
    medium_count: int = Field(ge=0)
    high_count: int = Field(ge=0)
    critical_count: int = Field(ge=0)
    highest_risk_score: int = Field(ge=0, le=100)
    average_risk_score: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_level_total(self) -> "RiskRunSummary":
        counted = (
            self.none_count
            + self.low_count
            + self.medium_count
            + self.high_count
            + self.critical_count
        )
        if counted != self.total_tests:
            raise ValueError("risk level counts must equal total_tests")
        return self
