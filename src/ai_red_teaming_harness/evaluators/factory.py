"""Evaluator selection by YAML configuration name."""

from __future__ import annotations

from .base import ResponseEvaluator
from .forbidden_patterns import ForbiddenPatternsEvaluator
from .refusal_quality import RefusalQualityEvaluator
from .regex_forbidden import RegexForbiddenEvaluator
from .required_patterns import RequiredPatternsEvaluator
from .response_length import ResponseLengthEvaluator
from .response_presence import ResponsePresenceEvaluator


EVALUATOR_FACTORIES: dict[str, type[ResponseEvaluator]] = {
    "forbidden_patterns": ForbiddenPatternsEvaluator,
    "refusal_quality": RefusalQualityEvaluator,
    "response_presence": ResponsePresenceEvaluator,
    "regex_forbidden": RegexForbiddenEvaluator,
    "required_patterns": RequiredPatternsEvaluator,
    "response_length": ResponseLengthEvaluator,
}


def get_evaluator(name: str) -> ResponseEvaluator | None:
    factory = EVALUATOR_FACTORIES.get(name.strip().lower())
    return factory() if factory is not None else None
