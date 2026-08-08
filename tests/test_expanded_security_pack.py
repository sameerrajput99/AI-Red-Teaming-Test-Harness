"""Tests for Day 8 expanded security test coverage."""

from __future__ import annotations

from pathlib import Path

from ai_red_teaming_harness.comparisons.engine import compare_evaluated_records
from ai_red_teaming_harness.comparisons.summary import build_comparison_summary
from ai_red_teaming_harness.evaluators.engine import evaluate_test_pack
from ai_red_teaming_harness.gates.engine import evaluate_security_gate
from ai_red_teaming_harness.gates.loader import load_gate_policy
from ai_red_teaming_harness.gates.models import GateStatus
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.models import Category, EvaluationVerdict
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPANDED_PACK = PROJECT_ROOT / "test_packs" / "day8_expanded_security_pack.yaml"
STRICT_POLICY = PROJECT_ROOT / "policies" / "strict_gate.yaml"


def _evaluated(provider_name: str):
    pack = load_test_pack(EXPANDED_PACK)
    executions = run_test_pack(pack, get_provider(provider_name))
    return pack, evaluate_test_pack(pack, executions)


def test_expanded_pack_loads_fourteen_unique_tests() -> None:
    pack = load_test_pack(EXPANDED_PACK)

    ids = [case.id for case in pack.test_cases]

    assert len(pack.test_cases) == 14
    assert len(ids) == len(set(ids))


def test_expanded_pack_covers_all_supported_categories() -> None:
    pack = load_test_pack(EXPANDED_PACK)

    categories = {case.category for case in pack.test_cases}

    assert categories == set(Category)


def test_vulnerable_baseline_fails_twelve_adversarial_tests() -> None:
    _, records = _evaluated("mock-vulnerable")

    verdicts = [record.security_verdict for record in records]

    assert verdicts.count(EvaluationVerdict.FAIL) == 12
    assert verdicts.count(EvaluationVerdict.PASS) == 2
    assert verdicts.count(EvaluationVerdict.REVIEW) == 0
    assert verdicts.count(EvaluationVerdict.ERROR) == 0


def test_hardened_candidate_passes_all_expanded_tests() -> None:
    _, records = _evaluated("mock-hardened")

    assert len(records) == 14
    assert all(
        record.security_verdict is EvaluationVerdict.PASS
        for record in records
    )


def test_expanded_comparison_shows_twelve_improvements() -> None:
    pack, baseline = _evaluated("mock-vulnerable")
    _, candidate = _evaluated("mock-hardened")

    comparisons = compare_evaluated_records(pack, baseline, candidate)
    summary = build_comparison_summary(pack, comparisons)

    assert summary.total_comparisons == 14
    assert summary.improved_count == 12
    assert summary.regressed_count == 0
    assert summary.unchanged_pass_count == 2
    assert summary.unchanged_issue_count == 0
    assert summary.indeterminate_count == 0


def test_strict_gate_passes_expanded_security_pack() -> None:
    pack, baseline = _evaluated("mock-vulnerable")
    _, candidate = _evaluated("mock-hardened")
    comparisons = compare_evaluated_records(pack, baseline, candidate)
    summary = build_comparison_summary(pack, comparisons)
    policy = load_gate_policy(STRICT_POLICY)

    result = evaluate_security_gate(policy, summary, comparisons)

    assert result.gate_status is GateStatus.PASSED
