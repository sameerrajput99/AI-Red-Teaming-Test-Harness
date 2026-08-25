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
from .matching import find_literal_matches, normalize_patterns


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
        values = normalize_patterns(config.values)

        if not values:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.REVIEW,
                reason="No required patterns were configured; human review is required.",
                matched_values=[],
            )

        matched = find_literal_matches(
            response,
            values,
            case_sensitive=config.case_sensitive,
            match_scope=config.match_scope,
        )

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
