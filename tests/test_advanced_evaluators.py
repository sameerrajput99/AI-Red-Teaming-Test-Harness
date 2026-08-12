"""Tests for Day 10 advanced deterministic evaluators."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from ai_red_teaming_harness.evaluators.engine import combine_findings, evaluate_test_pack
from ai_red_teaming_harness.evaluators.factory import EVALUATOR_FACTORIES
from ai_red_teaming_harness.evaluators.regex_forbidden import RegexForbiddenEvaluator
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.models import (
    EvaluationFinding,
    EvaluationVerdict,
    EvaluatorConfig,
)
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ADVANCED_PACK = PROJECT_ROOT / "test_packs" / "day10_advanced_evaluator_pack.yaml"


def _evaluated(provider_name: str):
    pack = load_test_pack(ADVANCED_PACK)
    executions = run_test_pack(pack, get_provider(provider_name))
    return pack, executions, evaluate_test_pack(pack, executions)


def test_response_length_config_rejects_reversed_bounds() -> None:
    with pytest.raises(ValidationError):
        EvaluatorConfig(
            type="response_length",
            minimum_response_chars=500,
            maximum_response_chars=100,
        )


def test_factory_registers_three_day10_evaluators() -> None:
    assert "regex_forbidden" in EVALUATOR_FACTORIES
    assert "required_patterns" in EVALUATOR_FACTORIES
    assert "response_length" in EVALUATOR_FACTORIES


def test_invalid_regular_expression_returns_review() -> None:
    pack = load_test_pack(ADVANCED_PACK)
    executions = run_test_pack(pack, get_provider("mock-vulnerable"))
    test_case = pack.test_cases[0]
    execution = executions[0]
    config = EvaluatorConfig(
        type="regex_forbidden",
        values=["("],
    )

    finding = RegexForbiddenEvaluator().evaluate(
        test_case,
        execution,
        config,
    )

    assert finding.verdict is EvaluationVerdict.REVIEW
    assert "invalid" in finding.reason.lower()


def test_required_patterns_and_length_pass_benign_control() -> None:
    _, _, records = _evaluated("mock-hardened")
    record = next(
        item for item in records
        if item.execution.test_id == "REQ-001"
    )

    assert record.security_verdict is EvaluationVerdict.PASS
    assert {finding.evaluator_type for finding in record.findings} == {
        "required_patterns",
        "response_length",
    }


def test_composite_precedence_is_error_fail_review_pass() -> None:
    def finding(verdict: EvaluationVerdict) -> EvaluationFinding:
        return EvaluationFinding(
            evaluator_type="demo",
            verdict=verdict,
            reason="Deterministic Day 10 precedence test.",
            matched_values=[],
        )

    assert combine_findings([finding(EvaluationVerdict.PASS)]) is EvaluationVerdict.PASS
    assert combine_findings([
        finding(EvaluationVerdict.PASS),
        finding(EvaluationVerdict.REVIEW),
    ]) is EvaluationVerdict.REVIEW
    assert combine_findings([
        finding(EvaluationVerdict.REVIEW),
        finding(EvaluationVerdict.FAIL),
    ]) is EvaluationVerdict.FAIL
    assert combine_findings([
        finding(EvaluationVerdict.FAIL),
        finding(EvaluationVerdict.ERROR),
    ]) is EvaluationVerdict.ERROR


def test_advanced_pack_expected_provider_verdicts() -> None:
    _, _, vulnerable = _evaluated("mock-vulnerable")
    _, _, hardened = _evaluated("mock-hardened")

    vulnerable_verdicts = [
        record.security_verdict for record in vulnerable
    ]
    hardened_verdicts = [
        record.security_verdict for record in hardened
    ]

    assert vulnerable_verdicts.count(EvaluationVerdict.FAIL) == 2
    assert vulnerable_verdicts.count(EvaluationVerdict.PASS) == 2
    assert all(
        verdict is EvaluationVerdict.PASS
        for verdict in hardened_verdicts
    )
