"""Tests for Day 7 policy-as-code security gating."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from ai_red_teaming_harness.comparisons.engine import compare_evaluated_records
from ai_red_teaming_harness.comparisons.summary import build_comparison_summary
from ai_red_teaming_harness.evaluators.engine import evaluate_test_pack
from ai_red_teaming_harness.gates.engine import evaluate_security_gate
from ai_red_teaming_harness.gates.loader import load_gate_policy
from ai_red_teaming_harness.gates.models import GatePolicy, GateStatus
from ai_red_teaming_harness.gates.workflow import generate_gate_artifacts
from ai_red_teaming_harness.loader import load_test_pack
from ai_red_teaming_harness.models import (
    ComparisonOutcome,
    ControlType,
    EvaluationVerdict,
)
from ai_red_teaming_harness.providers.factory import get_provider
from ai_red_teaming_harness.runner import run_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PACK = PROJECT_ROOT / "test_packs" / "day1_test_cases.yaml"
STRICT_POLICY = PROJECT_ROOT / "policies" / "strict_gate.yaml"


def _evaluated(provider_name: str):
    pack = load_test_pack(VALID_PACK)
    executions = run_test_pack(pack, get_provider(provider_name))
    return pack, evaluate_test_pack(pack, executions)


def _comparison(baseline_name: str, candidate_name: str):
    pack, baseline = _evaluated(baseline_name)
    _, candidate = _evaluated(candidate_name)
    records = compare_evaluated_records(pack, baseline, candidate)
    summary = build_comparison_summary(pack, records)
    return pack, baseline, candidate, records, summary


def test_policy_loader_reads_strict_policy() -> None:
    policy = load_gate_policy(STRICT_POLICY)

    assert policy.name == "strict_local_security_gate"
    assert policy.max_regressed == 0
    assert policy.minimum_improvements == 2
    assert policy.require_no_benign_regressions is True


def test_forward_comparison_passes_strict_gate() -> None:
    _, _, _, records, summary = _comparison(
        "mock-vulnerable",
        "mock-hardened",
    )
    policy = load_gate_policy(STRICT_POLICY)

    result = evaluate_security_gate(policy, summary, records)

    assert result.gate_status is GateStatus.PASSED
    assert all(rule.passed for rule in result.rule_results)


def test_reverse_comparison_fails_regression_rules() -> None:
    _, _, _, records, summary = _comparison(
        "mock-hardened",
        "mock-vulnerable",
    )
    policy = load_gate_policy(STRICT_POLICY)

    result = evaluate_security_gate(policy, summary, records)
    failed_ids = {rule.rule_id for rule in result.rule_results if not rule.passed}

    assert result.gate_status is GateStatus.FAILED
    assert "max_regressed" in failed_ids
    assert "max_candidate_failures" in failed_ids


def test_minimum_improvement_threshold_can_fail() -> None:
    _, _, _, records, summary = _comparison(
        "mock-vulnerable",
        "mock-hardened",
    )
    policy = GatePolicy(
        name="three_improvements_required",
        version="1.0",
        description="Require more improvements than the starter comparison provides.",
        minimum_improvements=3,
    )

    result = evaluate_security_gate(policy, summary, records)

    assert result.gate_status is GateStatus.FAILED
    improvement_rule = next(
        rule for rule in result.rule_results
        if rule.rule_id == "minimum_improvements"
    )
    assert improvement_rule.observed == 2
    assert improvement_rule.passed is False


def test_benign_regression_is_detected() -> None:
    _, _, _, records, summary = _comparison(
        "mock-vulnerable",
        "mock-hardened",
    )
    benign = records[2].model_copy(
        update={
            "control_type": ControlType.BENIGN,
            "candidate_verdict": EvaluationVerdict.FAIL,
            "outcome": ComparisonOutcome.REGRESSED,
        }
    )
    changed_records = [records[0], records[1], benign]
    changed_summary = summary.model_copy(
        update={
            "regressed_count": 1,
            "unchanged_pass_count": 0,
            "candidate_pass_count": 2,
            "candidate_fail_count": 1,
        }
    )
    policy = load_gate_policy(STRICT_POLICY)

    result = evaluate_security_gate(policy, changed_summary, changed_records)
    benign_rule = next(
        rule for rule in result.rule_results
        if rule.rule_id == "no_benign_regressions"
    )

    assert result.gate_status is GateStatus.FAILED
    assert benign_rule.observed == 1
    assert benign_rule.passed is False


def test_gate_workflow_writes_machine_readable_evidence(tmp_path: Path) -> None:
    pack, baseline, candidate, _, _ = _comparison(
        "mock-vulnerable",
        "mock-hardened",
    )
    policy = load_gate_policy(STRICT_POLICY)

    artifacts = generate_gate_artifacts(
        pack,
        baseline,
        candidate,
        policy,
        output_root=tmp_path,
    )
    payload = json.loads(artifacts.gate_report.read_text(encoding="utf-8"))

    assert artifacts.gate_result.gate_status is GateStatus.PASSED
    assert artifacts.gate_report.name == "gate_result.json"
    assert payload["schema_version"] == "1.0"
    assert payload["gate_result"]["gate_status"] == "PASSED"
    assert len(payload["gate_result"]["rule_results"]) == 6
