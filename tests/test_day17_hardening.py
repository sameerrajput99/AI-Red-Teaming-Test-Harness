"""Tests for Day 17 code quality, false-positive controls, and error hardening."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ai_red_teaming_harness.evaluators.base import ResponseEvaluator
from ai_red_teaming_harness.evaluators.engine import evaluate_execution, evaluate_test_pack
from ai_red_teaming_harness.evaluators.factory import EVALUATOR_FACTORIES
from ai_red_teaming_harness.evaluators.forbidden_patterns import ForbiddenPatternsEvaluator
from ai_red_teaming_harness.evaluators.required_patterns import RequiredPatternsEvaluator
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.models import (
    EvaluatorConfig,
    EvaluationFinding,
    EvaluationVerdict,
    ExecutionRecord,
    ExecutionStatus,
    ProviderResponse,
)
from ai_red_teaming_harness.providers.base import ChatProvider
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import MAX_PROVIDER_ERROR_DETAIL_CHARS, run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
HARDENING_PACK = PROJECT_ROOT / "test_packs" / "day17_hardening_pack.yaml"


def _execution(test_id: str, response: str) -> ExecutionRecord:
    return ExecutionRecord(
        run_id="RUN-DAY17-HARDENING",
        test_id=test_id,
        provider_name="day17-test-provider",
        prompt="A valid Day 17 test prompt.",
        response=response,
        execution_status=ExecutionStatus.SUCCESS,
        latency_ms=1,
        error_message=None,
        timestamp=datetime.now(timezone.utc),
    )


def test_word_scope_prevents_substring_false_positive() -> None:
    test_case = load_test_pack(HARDENING_PACK).test_cases[0]
    finding = ForbiddenPatternsEvaluator().evaluate(
        test_case,
        _execution("QLT-001", "A keyboard is an input device."),
        EvaluatorConfig(
            type="forbidden_patterns",
            values=["key"],
            match_scope="word",
        ),
    )

    assert finding.verdict is EvaluationVerdict.PASS
    assert finding.matched_values == []


def test_word_scope_still_detects_standalone_pattern() -> None:
    test_case = load_test_pack(HARDENING_PACK).test_cases[0]
    finding = ForbiddenPatternsEvaluator().evaluate(
        test_case,
        _execution("QLT-001", "The exposed key must be rotated."),
        EvaluatorConfig(
            type="forbidden_patterns",
            values=["key"],
            match_scope="word",
        ),
    )

    assert finding.verdict is EvaluationVerdict.FAIL
    assert finding.matched_values == ["key"]


def test_forbidden_pattern_honors_case_sensitive() -> None:
    test_case = load_test_pack(HARDENING_PACK).test_cases[0]
    finding = ForbiddenPatternsEvaluator().evaluate(
        test_case,
        _execution("QLT-001", "secret"),
        EvaluatorConfig(
            type="forbidden_patterns",
            values=["SECRET"],
            case_sensitive=True,
        ),
    )

    assert finding.verdict is EvaluationVerdict.PASS


def test_required_word_scope_rejects_partial_match() -> None:
    test_case = load_test_pack(HARDENING_PACK).test_cases[1]
    finding = RequiredPatternsEvaluator().evaluate(
        test_case,
        _execution(
            "QLT-002",
            "Reauthentication and preauthorization are workflow labels.",
        ),
        EvaluatorConfig(
            type="required_patterns",
            values=["authentication", "authorization"],
            match_mode="all",
            match_scope="word",
        ),
    )

    assert finding.verdict is EvaluationVerdict.FAIL
    assert finding.matched_values == []


class ExplodingEvaluator(ResponseEvaluator):
    @property
    def type_name(self) -> str:
        return "exploding"

    def evaluate(
        self,
        test_case,
        execution,
        config,
    ) -> EvaluationFinding:
        raise RuntimeError("API_KEY=SHOULD-NOT-LEAK")


def test_evaluator_exception_becomes_error_finding(monkeypatch) -> None:
    pack = load_test_pack(HARDENING_PACK)
    test_case = pack.test_cases[0].model_copy(
        update={"evaluators": [EvaluatorConfig(type="exploding")]}
    )
    monkeypatch.setitem(EVALUATOR_FACTORIES, "exploding", ExplodingEvaluator)

    result = evaluate_execution(
        test_case,
        _execution("QLT-001", "A normal provider response."),
    )

    assert result.security_verdict is EvaluationVerdict.ERROR
    assert result.findings[0].evaluator_type == "exploding"
    assert "SHOULD-NOT-LEAK" not in result.findings[0].reason


class SecretErrorProvider(ChatProvider):
    @property
    def name(self) -> str:
        return "secret-error-provider"

    def generate(self, prompt: str) -> ProviderResponse:
        raise RuntimeError("API_KEY=ULTRASECRET999")


def test_provider_error_redacts_secret() -> None:
    records = run_test_pack(load_test_pack(HARDENING_PACK), SecretErrorProvider())

    assert all("ULTRASECRET999" not in record.error_message for record in records)
    assert all("[REDACTED_SECRET]" in record.error_message for record in records)


class LongErrorProvider(ChatProvider):
    @property
    def name(self) -> str:
        return "long-error-provider"

    def generate(self, prompt: str) -> ProviderResponse:
        raise RuntimeError("x" * 5_000)


def test_provider_error_message_is_bounded() -> None:
    records = run_test_pack(load_test_pack(HARDENING_PACK), LongErrorProvider())

    maximum_length = len("RuntimeError: ") + MAX_PROVIDER_ERROR_DETAIL_CHARS
    assert all(len(record.error_message) <= maximum_length for record in records)


def test_day17_pack_provider_matrix() -> None:
    pack = load_test_pack(HARDENING_PACK)
    vulnerable = evaluate_test_pack(
        pack,
        run_test_pack(pack, get_provider("mock-vulnerable")),
    )
    hardened = evaluate_test_pack(
        pack,
        run_test_pack(pack, get_provider("mock-hardened")),
    )

    assert [item.security_verdict for item in vulnerable] == [
        EvaluationVerdict.FAIL,
        EvaluationVerdict.PASS,
        EvaluationVerdict.PASS,
    ]
    assert all(
        item.security_verdict is EvaluationVerdict.PASS
        for item in hardened
    )
