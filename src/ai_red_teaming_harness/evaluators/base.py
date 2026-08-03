"""Common evaluator contract for response-level security checks."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import EvaluationFinding, EvaluatorConfig, ExecutionRecord, TestCase


class ResponseEvaluator(ABC):
    """Contract implemented by every response evaluator."""

    @property
    @abstractmethod
    def type_name(self) -> str:
        """Return the evaluator name used in YAML configuration."""

    @abstractmethod
    def evaluate(
        self,
        test_case: TestCase,
        execution: ExecutionRecord,
        config: EvaluatorConfig,
    ) -> EvaluationFinding:
        """Inspect one response and return one structured finding."""
