"""Typed models for safe-export sanitization metadata."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SanitizationSummary(BaseModel):
    """Metadata describing what the safe-export sanitizer changed."""

    model_config = ConfigDict(extra="forbid")

    policy_name: str = Field(min_length=3, max_length=100)
    total_redactions: int = Field(ge=0)
    redactions_by_rule: dict[str, int]
    raw_response_exported: bool = False
    raw_prompt_exported: bool = False
