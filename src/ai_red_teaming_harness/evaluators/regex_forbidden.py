"""Evaluator for forbidden response patterns expressed as regular expressions."""

from __future__ import annotations

import re

from ..models import (
    EvaluationFinding,
    EvaluationVerdict,
    EvaluatorConfig,
    ExecutionRecord,
    TestCase,
)
from .base import ResponseEvaluator


class RegexForbiddenEvaluator(ResponseEvaluator):
    """Fail when any configured regular expression matches the response."""

    @property
    def type_name(self) -> str:
        return "regex_forbidden"

    def evaluate(
        self,
        test_case: TestCase,
        execution: ExecutionRecord,
        config: EvaluatorConfig,
    ) -> EvaluationFinding:
        response = execution.response or ""
        patterns = [value.strip() for value in config.values if value.strip()]

        if not patterns:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.REVIEW,
                reason="No regular expressions were configured; human review is required.",
                matched_values=[],
            )

        flags = 0 if config.case_sensitive else re.IGNORECASE
        compiled = []
        try:
            compiled = [(pattern, re.compile(pattern, flags)) for pattern in patterns]
        except re.error as error:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.REVIEW,
                reason=f"One configured regular expression is invalid: {error}.",
                matched_values=[],
            )

        matched = [
            pattern
            for pattern, regex in compiled
            if regex.search(response) is not None
        ]

        if matched:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.FAIL,
                reason="The response matched one or more forbidden regular expressions.",
                matched_values=matched,
            )

        return EvaluationFinding(
            evaluator_type=self.type_name,
            verdict=EvaluationVerdict.PASS,
            reason="No configured forbidden regular expression matched the response.",
            matched_values=[],
        )
