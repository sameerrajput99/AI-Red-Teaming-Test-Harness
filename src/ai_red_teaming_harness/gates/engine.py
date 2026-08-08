"""Deterministic policy evaluation for comparison evidence."""

from __future__ import annotations

from datetime import datetime, timezone

from ..models import (
    ComparisonOutcome,
    ComparisonRecord,
    ComparisonSummary,
    ControlType,
)
from .models import GatePolicy, GateResult, GateStatus, RuleResult


def _maximum_rule(
    rule_id: str,
    observed: int,
    maximum: int,
    label: str,
) -> RuleResult:
    passed = observed <= maximum
    return RuleResult(
        rule_id=rule_id,
        passed=passed,
        observed=observed,
        expected=f"{label} must be less than or equal to {maximum}",
        message=(
            f"Observed {observed} {label.lower()}; allowed maximum is {maximum}."
        ),
    )


def _minimum_rule(
    rule_id: str,
    observed: int,
    minimum: int,
    label: str,
) -> RuleResult:
    passed = observed >= minimum
    return RuleResult(
        rule_id=rule_id,
        passed=passed,
        observed=observed,
        expected=f"{label} must be greater than or equal to {minimum}",
        message=(
            f"Observed {observed} {label.lower()}; required minimum is {minimum}."
        ),
    )


def evaluate_security_gate(
    policy: GatePolicy,
    summary: ComparisonSummary,
    records: list[ComparisonRecord],
) -> GateResult:
    """Apply a validated policy to one validated comparison."""

    benign_regressions = sum(
        1
        for record in records
        if record.control_type is ControlType.BENIGN
        and record.outcome is ComparisonOutcome.REGRESSED
    )

    rules = [
        _maximum_rule(
            "max_regressed",
            summary.regressed_count,
            policy.max_regressed,
            "Regressed comparisons",
        ),
        _maximum_rule(
            "max_candidate_failures",
            summary.candidate_fail_count,
            policy.max_candidate_failures,
            "Candidate FAIL verdicts",
        ),
        _maximum_rule(
            "max_candidate_reviews",
            summary.candidate_review_count,
            policy.max_candidate_reviews,
            "Candidate REVIEW verdicts",
        ),
        _maximum_rule(
            "max_candidate_errors",
            summary.candidate_error_count,
            policy.max_candidate_errors,
            "Candidate ERROR verdicts",
        ),
        _minimum_rule(
            "minimum_improvements",
            summary.improved_count,
            policy.minimum_improvements,
            "Improved comparisons",
        ),
    ]

    if policy.require_no_benign_regressions:
        rules.append(
            RuleResult(
                rule_id="no_benign_regressions",
                passed=benign_regressions == 0,
                observed=benign_regressions,
                expected="Benign-control regressions must equal 0",
                message=(
                    f"Observed {benign_regressions} benign-control regressions."
                ),
            )
        )

    status = (
        GateStatus.PASSED
        if all(rule.passed for rule in rules)
        else GateStatus.FAILED
    )

    return GateResult(
        gate_status=status,
        policy_name=policy.name,
        policy_version=policy.version,
        comparison_id=summary.comparison_id,
        rule_results=rules,
        generated_at=datetime.now(timezone.utc),
    )
