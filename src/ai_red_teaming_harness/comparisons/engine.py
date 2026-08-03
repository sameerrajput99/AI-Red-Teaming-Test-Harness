"""Align and compare evaluated records from two provider configurations."""

from __future__ import annotations

from collections import defaultdict

from ..models import (
    ComparisonOutcome,
    ComparisonRecord,
    EvaluatedRecord,
    EvaluationVerdict,
    TestPack,
)


VERDICT_RISK = {
    EvaluationVerdict.PASS: 0,
    EvaluationVerdict.REVIEW: 1,
    EvaluationVerdict.FAIL: 2,
}


def classify_outcome(
    baseline: EvaluationVerdict,
    candidate: EvaluationVerdict,
) -> ComparisonOutcome:
    """Classify how one candidate verdict changed from its baseline verdict."""

    if EvaluationVerdict.ERROR in {baseline, candidate}:
        return ComparisonOutcome.INDETERMINATE
    if baseline is EvaluationVerdict.PASS and candidate is EvaluationVerdict.PASS:
        return ComparisonOutcome.UNCHANGED_PASS
    if baseline is candidate:
        return ComparisonOutcome.UNCHANGED_ISSUE

    baseline_risk = VERDICT_RISK[baseline]
    candidate_risk = VERDICT_RISK[candidate]
    if candidate_risk < baseline_risk:
        return ComparisonOutcome.IMPROVED
    if candidate_risk > baseline_risk:
        return ComparisonOutcome.REGRESSED
    return ComparisonOutcome.INDETERMINATE


def _explanation(
    baseline: EvaluationVerdict,
    candidate: EvaluationVerdict,
    outcome: ComparisonOutcome,
) -> str:
    transition = f"{baseline.value} to {candidate.value}"
    messages = {
        ComparisonOutcome.IMPROVED: (
            f"The candidate improved from {transition} for the same configured test."
        ),
        ComparisonOutcome.REGRESSED: (
            f"The candidate regressed from {transition} for the same configured test."
        ),
        ComparisonOutcome.UNCHANGED_PASS: (
            "Both configurations passed the same configured test."
        ),
        ComparisonOutcome.UNCHANGED_ISSUE: (
            f"Both configurations retained the same non-pass verdict: {baseline.value}."
        ),
        ComparisonOutcome.INDETERMINATE: (
            "At least one side produced an error, so the security change is indeterminate."
        ),
    }
    return messages[outcome]


def _group_records(records: list[EvaluatedRecord]) -> dict[str, list[EvaluatedRecord]]:
    grouped: dict[str, list[EvaluatedRecord]] = defaultdict(list)
    for record in records:
        grouped[record.execution.test_id].append(record)
    return dict(grouped)


def compare_evaluated_records(
    test_pack: TestPack,
    baseline_records: list[EvaluatedRecord],
    candidate_records: list[EvaluatedRecord],
) -> list[ComparisonRecord]:
    """Align equivalent test attempts and produce side-by-side comparisons."""

    if not baseline_records or not candidate_records:
        raise ValueError("Both baseline and candidate records are required")

    baseline_providers = {record.execution.provider_name for record in baseline_records}
    candidate_providers = {record.execution.provider_name for record in candidate_records}
    baseline_run_ids = {record.execution.run_id for record in baseline_records}
    candidate_run_ids = {record.execution.run_id for record in candidate_records}

    if len(baseline_providers) != 1 or len(candidate_providers) != 1:
        raise ValueError("Each comparison side must contain records from one provider")
    if len(baseline_run_ids) != 1 or len(candidate_run_ids) != 1:
        raise ValueError("Each comparison side must contain records from one run_id")

    baseline_provider = next(iter(baseline_providers))
    candidate_provider = next(iter(candidate_providers))
    if baseline_provider == candidate_provider:
        raise ValueError("Baseline and candidate providers must be different")

    baseline_by_id = _group_records(baseline_records)
    candidate_by_id = _group_records(candidate_records)
    expected_ids = {case.id for case in test_pack.test_cases}

    if set(baseline_by_id) != expected_ids:
        raise ValueError("Baseline records do not match the validated test pack")
    if set(candidate_by_id) != expected_ids:
        raise ValueError("Candidate records do not match the validated test pack")

    comparisons: list[ComparisonRecord] = []
    for test_case in test_pack.test_cases:
        baseline_attempts = baseline_by_id[test_case.id]
        candidate_attempts = candidate_by_id[test_case.id]
        if len(baseline_attempts) != len(candidate_attempts):
            raise ValueError(
                f"Attempt count mismatch for {test_case.id}: "
                f"baseline={len(baseline_attempts)}, candidate={len(candidate_attempts)}"
            )

        for attempt, (baseline, candidate) in enumerate(
            zip(baseline_attempts, candidate_attempts, strict=True),
            start=1,
        ):
            outcome = classify_outcome(
                baseline.security_verdict,
                candidate.security_verdict,
            )
            comparisons.append(
                ComparisonRecord(
                    test_id=test_case.id,
                    attempt=attempt,
                    title=test_case.title,
                    category=test_case.category,
                    control_type=test_case.control_type,
                    severity=test_case.severity,
                    baseline_provider=baseline_provider,
                    candidate_provider=candidate_provider,
                    baseline_run_id=baseline.execution.run_id,
                    candidate_run_id=candidate.execution.run_id,
                    baseline_verdict=baseline.security_verdict,
                    candidate_verdict=candidate.security_verdict,
                    outcome=outcome,
                    baseline_response=baseline.execution.response,
                    candidate_response=candidate.execution.response,
                    explanation=_explanation(
                        baseline.security_verdict,
                        candidate.security_verdict,
                        outcome,
                    ),
                )
            )

    return comparisons
