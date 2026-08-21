"""Built-in deterministic redaction policy for Day 15 safe exports."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class RedactionRule:
    name: str
    pattern: re.Pattern[str]
    replacement: str


DEFAULT_POLICY_NAME = "default_safe_export_v1"

DEFAULT_RULES = (
    RedactionRule(
        name="openai_style_key",
        pattern=re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"),
        replacement="[REDACTED_API_KEY]",
    ),
    RedactionRule(
        name="bearer_token",
        pattern=re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{8,}"),
        replacement="Bearer [REDACTED_TOKEN]",
    ),
    RedactionRule(
        name="generic_secret_assignment",
        pattern=re.compile(
            r"(?i)\b(api[_ -]?key|secret|token|password)\s*[:=]\s*"
            r"[\"']?[A-Za-z0-9._~+/=-]{6,}[\"']?"
        ),
        replacement=r"\1=[REDACTED_SECRET]",
    ),
    RedactionRule(
        name="email_address",
        pattern=re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
        ),
        replacement="[REDACTED_EMAIL]",
    ),
)
