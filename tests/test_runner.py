"""Tests for Day 2 provider abstraction and raw test execution."""

from __future__ import annotations

from pathlib import Path

from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.models import ExecutionStatus, ProviderResponse
from ai_red_teaming_harness.providers.base import ChatProvider
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PACK = PROJECT_ROOT / "test_packs" / "day1_test_cases.yaml"


def test_vulnerable_provider_runs_all_three_cases() -> None:
    pack = load_test_pack(VALID_PACK)
    provider = get_provider("mock-vulnerable")

    records = run_test_pack(pack, provider)

    assert len(records) == 3
    assert all(record.execution_status is ExecutionStatus.SUCCESS for record in records)
    assert len({record.run_id for record in records}) == 1
    assert "SYSTEM_PROMPT:" in records[0].response


def test_hardened_provider_refuses_attack_and_answers_control() -> None:
    pack = load_test_pack(VALID_PACK)
    provider = get_provider("mock-hardened")

    records = run_test_pack(pack, provider)

    assert "cannot reveal internal instructions" in records[0].response.lower()
    assert "machine learning" in records[2].response.lower()


def test_unknown_provider_is_rejected() -> None:
    try:
        get_provider("not-a-provider")
    except ValueError as error:
        assert "Unknown provider" in str(error)
    else:
        raise AssertionError("Unknown provider should raise ValueError")


class BrokenProvider(ChatProvider):
    @property
    def name(self) -> str:
        return "broken-provider"

    def generate(self, prompt: str) -> ProviderResponse:
        raise TimeoutError("simulated provider timeout")


def test_runner_records_provider_errors_without_crashing_pack() -> None:
    pack = load_test_pack(VALID_PACK)

    records = run_test_pack(pack, BrokenProvider())

    assert len(records) == 3
    assert all(record.execution_status is ExecutionStatus.ERROR for record in records)
    assert all("TimeoutError" in record.error_message for record in records)
