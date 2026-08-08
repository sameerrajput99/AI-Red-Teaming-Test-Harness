"""Typed models for security policy gates."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GateStatus(str, Enum):
    """Final decision produced by a security policy gate."""

    PASSED = "PASSED"
    FAILED = "FAILED"


class GatePolicy(BaseModel):
    """Strict, versioned thresholds for one candidate comparison."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=120)
    version: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=10, max_length=500)
    max_regressed: int = Field(default=0, ge=0)
    max_candidate_failures: int = Field(default=0, ge=0)
    max_candidate_reviews: int = Field(default=0, ge=0)
    max_candidate_errors: int = Field(default=0, ge=0)
    minimum_improvements: int = Field(default=0, ge=0)
    require_no_benign_regressions: bool = True


class GatePolicyDocument(BaseModel):
    """Top-level YAML document for a gate policy."""

    model_config = ConfigDict(extra="forbid")

    gate_policy: GatePolicy


class RuleResult(BaseModel):
    """One deterministic gate rule and its observed evidence."""

    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=3, max_length=100)
    passed: bool
    observed: Any
    expected: str = Field(min_length=2, max_length=200)
    message: str = Field(min_length=5, max_length=500)


class GateResult(BaseModel):
    """Final gate status with explainable rule-level evidence."""

    model_config = ConfigDict(extra="forbid")

    gate_status: GateStatus
    policy_name: str = Field(min_length=3, max_length=120)
    policy_version: str = Field(min_length=1, max_length=30)
    comparison_id: str = Field(min_length=12, max_length=90)
    rule_results: list[RuleResult] = Field(min_length=1)
    generated_at: datetime

    @model_validator(mode="after")
    def validate_status_matches_rules(self) -> "GateResult":
        all_passed = all(result.passed for result in self.rule_results)
        expected_status = GateStatus.PASSED if all_passed else GateStatus.FAILED
        if self.gate_status is not expected_status:
            raise ValueError("gate_status must match the combined rule results")
        return self
