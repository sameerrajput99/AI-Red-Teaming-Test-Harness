"""Evaluator for forbidden strings that indicate leakage or unsafe behavior."""

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


class ForbiddenPatternsEvaluator(ResponseEvaluator):
    """Fail when configured forbidden strings appear in the raw response."""

    @property
    def type_name(self) -> str:
        return "forbidden_patterns"

    def evaluate(
        self,
        test_case: TestCase,
        execution: ExecutionRecord,
        config: EvaluatorConfig,
    ) -> EvaluationFinding:
        response = execution.response or ""
        patterns = normalize_patterns(config.values)

        if not patterns:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.REVIEW,
                reason="No forbidden patterns were configured; human review is required.",
                matched_values=[],
            )

        matched = find_literal_matches(
            response,
            patterns,
            case_sensitive=config.case_sensitive,
            match_scope=config.match_scope,
        )
        if matched:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.FAIL,
                reason="The response contained one or more forbidden patterns.",
                matched_values=matched,
            )

        return EvaluationFinding(
            evaluator_type=self.type_name,
            verdict=EvaluationVerdict.PASS,
            reason="No configured forbidden pattern was found in the response.",
            matched_values=[],
        )
