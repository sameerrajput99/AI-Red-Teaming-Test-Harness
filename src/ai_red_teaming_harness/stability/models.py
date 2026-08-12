"""Typed models for repeated-run stability analysis."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..models import Category, ControlType, EvaluationVerdict, Severity


class StabilityStatus(str, Enum):
    """How consistent one test's verdicts were across repetitions."""

    STABLE_PASS = "STABLE_PASS"
    STABLE_FAIL = "STABLE_FAIL"
    STABLE_REVIEW = "STABLE_REVIEW"
    STABLE_ERROR = "STABLE_ERROR"
    FLAKY = "FLAKY"


class StabilityRecord(BaseModel):
    """Repeated-run metrics for one test case."""

    model_config = ConfigDict(extra="forbid")

    test_id: str = Field(min_length=5, max_length=30)
    title: str = Field(min_length=5, max_length=140)
    category: Category
    control_type: ControlType
    severity: Severity
    total_attempts: int = Field(ge=1)
    pass_count: int = Field(ge=0)
    fail_count: int = Field(ge=0)
    review_count: int = Field(ge=0)
    error_count: int = Field(ge=0)
    pass_rate_percent: float = Field(ge=0, le=100)
    verdicts_seen: list[EvaluationVerdict] = Field(min_length=1, max_length=4)
    status: StabilityStatus

    @model_validator(mode="after")
    def validate_counts(self) -> "StabilityRecord":
        total = (
            self.pass_count
            + self.fail_count
            + self.review_count
            + self.error_count
        )
        if total != self.total_attempts:
            raise ValueError("stability verdict counts must equal total_attempts")
        return self


class StabilityRunSummary(BaseModel):
    """Run-level repeated-execution stability metrics."""

    model_config = ConfigDict(extra="forbid")

    provider_name: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    total_tests: int = Field(ge=1)
    total_attempts: int = Field(ge=1)
    stable_pass_count: int = Field(ge=0)
    stable_issue_count: int = Field(ge=0)
    flaky_count: int = Field(ge=0)
    average_pass_rate_percent: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_test_counts(self) -> "StabilityRunSummary":
        if (
            self.stable_pass_count
            + self.stable_issue_count
            + self.flaky_count
            != self.total_tests
        ):
            raise ValueError("stability summary test counts must equal total_tests")
        return self
