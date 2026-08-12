"""Evaluator for phrases that should appear in an acceptable response."""

from __future__ import annotations

from ..models import (
    EvaluationFinding,
    EvaluationVerdict,
    EvaluatorConfig,
    ExecutionRecord,
    TestCase,
)
from .base import ResponseEvaluator


class RequiredPatternsEvaluator(ResponseEvaluator):
    """Require any or all configured phrases to appear in the response."""

    @property
    def type_name(self) -> str:
        return "required_patterns"

    def evaluate(
        self,
        test_case: TestCase,
        execution: ExecutionRecord,
        config: EvaluatorConfig,
    ) -> EvaluationFinding:
        response = execution.response or ""
        values = [value.strip() for value in config.values if value.strip()]

        if not values:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.REVIEW,
                reason="No required patterns were configured; human review is required.",
                matched_values=[],
            )

        haystack = response if config.case_sensitive else response.lower()
        matched = []
        for value in values:
            needle = value if config.case_sensitive else value.lower()
            if needle in haystack:
                matched.append(value)

        passed = (
            len(matched) == len(values)
            if config.match_mode == "all"
            else len(matched) >= 1
        )

        if passed:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.PASS,
                reason=(
                    f"Required pattern rule passed using match_mode={config.match_mode}."
                ),
                matched_values=matched,
            )

        verdict = (
            EvaluationVerdict.REVIEW
            if test_case.manual_review_if_uncertain
            else EvaluationVerdict.FAIL
        )
        return EvaluationFinding(
            evaluator_type=self.type_name,
            verdict=verdict,
            reason=(
                f"Required pattern rule did not pass using match_mode={config.match_mode}."
            ),
            matched_values=matched,
        )
