"""Typed data models for structured AI red teaming test cases and executions."""

from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Category(str, Enum):
    """Security categories supported by the starter schema."""

    PROMPT_LEAKAGE = "prompt_leakage"
    PROMPT_INJECTION = "prompt_injection"
    INSTRUCTION_OVERRIDE = "instruction_override"
    REFUSAL_BEHAVIOR = "refusal_behavior"
    HALLUCINATION = "hallucination"
    SAFETY_BOUNDARY = "safety_boundary"
    BENIGN_CONTROL = "benign_control"


class ControlType(str, Enum):
    """Whether a test is hostile or a normal usability control."""

    ADVERSARIAL = "adversarial"
    BENIGN = "benign"


class Severity(str, Enum):
    """Potential impact if the defined security behavior fails."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class ExecutionStatus(str, Enum):
    """Whether the provider call itself completed successfully."""

    SUCCESS = "success"
    ERROR = "error"


class EvaluationVerdict(str, Enum):
    """Security decision produced by response evaluators."""

    PASS = "PASS"
    FAIL = "FAIL"
    REVIEW = "REVIEW"
    ERROR = "ERROR"


class EvaluatorConfig(BaseModel):
    """Configuration for an evaluator that will be implemented later."""

    model_config = ConfigDict(extra="forbid")

    type: str = Field(min_length=2, max_length=80)
    values: list[str] = Field(default_factory=list)
    minimum_refusal_signals: int | None = Field(default=None, ge=0, le=10)

    @field_validator("type")
    @classmethod
    def normalize_type(cls, value: str) -> str:
        return value.strip().lower()


class TestCase(BaseModel):
    """Contract that every AI security test case must satisfy."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=5, max_length=30)
    title: str = Field(min_length=5, max_length=140)
    category: Category
    description: str = Field(min_length=10, max_length=500)
    control_type: ControlType
    prompt: str = Field(min_length=3, max_length=5000)
    expected_behavior: str = Field(min_length=3, max_length=120)
    severity: Severity
    tags: list[str] = Field(default_factory=list, max_length=20)
    evaluators: list[EvaluatorConfig] = Field(min_length=1)
    manual_review_if_uncertain: bool = True
    repetitions: int = Field(default=1, ge=1, le=20)

    @field_validator("id")
    @classmethod
    def validate_id_format(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not re.fullmatch(r"[A-Z]+-\d{3}", normalized):
            raise ValueError("id must use a format such as PL-001 or CTRL-001")
        return normalized

    @field_validator("expected_behavior")
    @classmethod
    def validate_expected_behavior(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.fullmatch(r"[a-z][a-z0-9_]*", normalized):
            raise ValueError("expected_behavior must use snake_case")
        return normalized

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, values: list[str]) -> list[str]:
        normalized = [value.strip().lower() for value in values if value.strip()]
        if len(normalized) != len(set(normalized)):
            raise ValueError("tags must not contain duplicates")
        return normalized

    @model_validator(mode="after")
    def validate_control_severity(self) -> "TestCase":
        if self.control_type is ControlType.BENIGN and self.severity not in {
            Severity.LOW,
            Severity.INFORMATIONAL,
        }:
            raise ValueError("benign controls should use low or informational severity")
        return self


class TestPackMetadata(BaseModel):
    """Human-readable metadata for a collection of tests."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=120)
    version: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=10, max_length=500)


class TestPack(BaseModel):
    """A validated collection of test cases."""

    model_config = ConfigDict(extra="forbid")

    test_pack: TestPackMetadata
    test_cases: list[TestCase] = Field(min_length=1)

    @model_validator(mode="after")
    def ensure_unique_test_ids(self) -> "TestPack":
        ids = [case.id for case in self.test_cases]
        if len(ids) != len(set(ids)):
            raise ValueError("test case ids must be unique inside a test pack")
        return self


class ProviderResponse(BaseModel):
    """Raw response returned by a chatbot provider adapter."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=20_000)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExecutionRecord(BaseModel):
    """Raw evidence captured when one test case is sent to one provider."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=8, max_length=80)
    test_id: str = Field(min_length=5, max_length=30)
    provider_name: str = Field(min_length=2, max_length=100)
    prompt: str = Field(min_length=3, max_length=5000)
    response: str | None = Field(default=None, max_length=20_000)
    execution_status: ExecutionStatus
    latency_ms: int = Field(ge=0)
    error_message: str | None = Field(default=None, max_length=2000)
    timestamp: datetime

    @model_validator(mode="after")
    def validate_status_fields(self) -> "ExecutionRecord":
        if self.execution_status is ExecutionStatus.SUCCESS:
            if not self.response:
                raise ValueError("successful executions must include a response")
            if self.error_message is not None:
                raise ValueError("successful executions must not include an error_message")

        if self.execution_status is ExecutionStatus.ERROR:
            if not self.error_message:
                raise ValueError("failed executions must include an error_message")

        return self


class EvaluationFinding(BaseModel):
    """One evaluator's structured decision and supporting reason."""

    model_config = ConfigDict(extra="forbid")

    evaluator_type: str = Field(min_length=2, max_length=80)
    verdict: EvaluationVerdict
    reason: str = Field(min_length=5, max_length=1000)
    matched_values: list[str] = Field(default_factory=list, max_length=50)


class EvaluatedRecord(BaseModel):
    """Raw execution evidence plus the final composite security verdict."""

    model_config = ConfigDict(extra="forbid")

    execution: ExecutionRecord
    security_verdict: EvaluationVerdict
    findings: list[EvaluationFinding] = Field(min_length=1)
    summary: str = Field(min_length=5, max_length=1000)


class RunSummary(BaseModel):
    """Validated run-level metrics used by evidence reporters."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=8, max_length=80)
    provider_name: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    test_pack_version: str = Field(min_length=1, max_length=30)
    total_tests: int = Field(ge=1)
    pass_count: int = Field(ge=0)
    fail_count: int = Field(ge=0)
    review_count: int = Field(ge=0)
    error_count: int = Field(ge=0)
    average_latency_ms: float = Field(ge=0)
    generated_at: datetime

    @model_validator(mode="after")
    def validate_verdict_total(self) -> "RunSummary":
        counted = (
            self.pass_count
            + self.fail_count
            + self.review_count
            + self.error_count
        )
        if counted != self.total_tests:
            raise ValueError("verdict counts must equal total_tests")
        return self


class ComparisonOutcome(str, Enum):
    """How the candidate verdict changed relative to the baseline."""

    IMPROVED = "IMPROVED"
    REGRESSED = "REGRESSED"
    UNCHANGED_PASS = "UNCHANGED_PASS"
    UNCHANGED_ISSUE = "UNCHANGED_ISSUE"
    INDETERMINATE = "INDETERMINATE"


class ComparisonRecord(BaseModel):
    """Side-by-side evidence for one test attempt across two providers."""

    model_config = ConfigDict(extra="forbid")

    test_id: str = Field(min_length=5, max_length=30)
    attempt: int = Field(ge=1)
    title: str = Field(min_length=5, max_length=140)
    category: Category
    control_type: ControlType
    severity: Severity
    baseline_provider: str = Field(min_length=2, max_length=100)
    candidate_provider: str = Field(min_length=2, max_length=100)
    baseline_run_id: str = Field(min_length=8, max_length=80)
    candidate_run_id: str = Field(min_length=8, max_length=80)
    baseline_verdict: EvaluationVerdict
    candidate_verdict: EvaluationVerdict
    outcome: ComparisonOutcome
    baseline_response: str | None = Field(default=None, max_length=20_000)
    candidate_response: str | None = Field(default=None, max_length=20_000)
    explanation: str = Field(min_length=5, max_length=1000)


class ComparisonSummary(BaseModel):
    """Aggregated metrics for one baseline-versus-candidate comparison."""

    model_config = ConfigDict(extra="forbid")

    comparison_id: str = Field(min_length=12, max_length=90)
    baseline_run_id: str = Field(min_length=8, max_length=80)
    candidate_run_id: str = Field(min_length=8, max_length=80)
    baseline_provider: str = Field(min_length=2, max_length=100)
    candidate_provider: str = Field(min_length=2, max_length=100)
    test_pack_name: str = Field(min_length=3, max_length=120)
    test_pack_version: str = Field(min_length=1, max_length=30)
    total_comparisons: int = Field(ge=1)
    improved_count: int = Field(ge=0)
    regressed_count: int = Field(ge=0)
    unchanged_pass_count: int = Field(ge=0)
    unchanged_issue_count: int = Field(ge=0)
    indeterminate_count: int = Field(ge=0)
    baseline_pass_count: int = Field(ge=0)
    baseline_fail_count: int = Field(ge=0)
    baseline_review_count: int = Field(ge=0)
    baseline_error_count: int = Field(ge=0)
    candidate_pass_count: int = Field(ge=0)
    candidate_fail_count: int = Field(ge=0)
    candidate_review_count: int = Field(ge=0)
    candidate_error_count: int = Field(ge=0)
    generated_at: datetime

    @model_validator(mode="after")
    def validate_outcome_total(self) -> "ComparisonSummary":
        counted = (
            self.improved_count
            + self.regressed_count
            + self.unchanged_pass_count
            + self.unchanged_issue_count
            + self.indeterminate_count
        )
        if counted != self.total_comparisons:
            raise ValueError("comparison outcome counts must equal total_comparisons")

        baseline_total = (
            self.baseline_pass_count
            + self.baseline_fail_count
            + self.baseline_review_count
            + self.baseline_error_count
        )
        candidate_total = (
            self.candidate_pass_count
            + self.candidate_fail_count
            + self.candidate_review_count
            + self.candidate_error_count
        )
        if baseline_total != self.total_comparisons:
            raise ValueError("baseline verdict counts must equal total_comparisons")
        if candidate_total != self.total_comparisons:
            raise ValueError("candidate verdict counts must equal total_comparisons")
        return self
