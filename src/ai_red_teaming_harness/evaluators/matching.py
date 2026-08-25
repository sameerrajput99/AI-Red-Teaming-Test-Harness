"""Shared literal-pattern matching helpers for deterministic evaluators."""

from __future__ import annotations

import re
from typing import Literal


MatchScope = Literal["substring", "word"]


def normalize_patterns(values: list[str]) -> list[str]:
    """Return stripped, non-empty patterns while preserving their order."""

    return [value.strip() for value in values if value.strip()]


def find_literal_matches(
    response: str,
    patterns: list[str],
    *,
    case_sensitive: bool,
    match_scope: MatchScope,
) -> list[str]:
    """Find configured literal patterns using explicit matching semantics."""

    normalized = normalize_patterns(patterns)
    flags = 0 if case_sensitive else re.IGNORECASE

    if match_scope == "word":
        return [
            pattern
            for pattern in normalized
            if re.search(
                rf"(?<!\w){re.escape(pattern)}(?!\w)",
                response,
                flags,
            )
            is not None
        ]

    haystack = response if case_sensitive else response.casefold()
    return [
        pattern
        for pattern in normalized
        if (pattern if case_sensitive else pattern.casefold()) in haystack
    ]
