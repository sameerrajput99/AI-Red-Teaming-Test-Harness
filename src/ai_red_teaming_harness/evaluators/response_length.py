"""Evaluator for configurable response-length boundaries."""

from __future__ import annotations

from ..models import (
    EvaluationFinding,
    EvaluationVerdict,
    EvaluatorConfig,
    ExecutionRecord,
    TestCase,
)
from .base import ResponseEvaluator


class ResponseLengthEvaluator(ResponseEvaluator):
    """Check whether response character length stays inside configured bounds."""

    @property
    def type_name(self) -> str:
        return "response_length"

    def evaluate(
        self,
        test_case: TestCase,
        execution: ExecutionRecord,
        config: EvaluatorConfig,
    ) -> EvaluationFinding:
        minimum = config.minimum_response_chars
        maximum = config.maximum_response_chars

        if minimum is None and maximum is None:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.REVIEW,
                reason="No response-length boundary was configured.",
                matched_values=[],
            )

        response = execution.response or ""
        length = len(response)

        too_short = minimum is not None and length < minimum
        too_long = maximum is not None and length > maximum

        if not too_short and not too_long:
            return EvaluationFinding(
                evaluator_type=self.type_name,
                verdict=EvaluationVerdict.PASS,
                reason=f"Response length {length} characters is within configured bounds.",
                matched_values=[str(length)],
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
                f"Response length {length} characters is outside configured bounds "
                f"(min={minimum}, max={maximum})."
            ),
            matched_values=[str(length)],
        )
