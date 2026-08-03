"""Evaluator selection by YAML configuration name."""

from __future__ import annotations

from .base import ResponseEvaluator
from .forbidden_patterns import ForbiddenPatternsEvaluator
from .refusal_quality import RefusalQualityEvaluator
from .response_presence import ResponsePresenceEvaluator


EVALUATOR_FACTORIES: dict[str, type[ResponseEvaluator]] = {
    "forbidden_patterns": ForbiddenPatternsEvaluator,
    "refusal_quality": RefusalQualityEvaluator,
    "response_presence": ResponsePresenceEvaluator,
}


def get_evaluator(name: str) -> ResponseEvaluator | None:
    """Return an evaluator instance, or None when the type is unsupported."""

    factory = EVALUATOR_FACTORIES.get(name.strip().lower())
    return factory() if factory is not None else None
