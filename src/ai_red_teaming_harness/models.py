"""Typed data models for structured AI red teaming test cases."""

from __future__ import annotations

import re
from enum import Enum

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
