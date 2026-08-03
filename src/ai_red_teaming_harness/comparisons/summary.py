"""Comparison-level summary calculations."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from uuid import uuid4

from ..models import (
    ComparisonOutcome,
    ComparisonRecord,
    ComparisonSummary,
    EvaluationVerdict,
    TestPack,
)


def build_comparison_summary(
    test_pack: TestPack,
    records: list[ComparisonRecord],
) -> ComparisonSummary:
    """Aggregate side-by-side comparison records into validated metrics."""

    if not records:
        raise ValueError("Cannot summarize an empty comparison-record list")

    baseline_runs = {record.baseline_run_id for record in records}
    candidate_runs = {record.candidate_run_id for record in records}
    baseline_providers = {record.baseline_provider for record in records}
    candidate_providers = {record.candidate_provider for record in records}
    if len(baseline_runs) != 1 or len(candidate_runs) != 1:
        raise ValueError("Comparison records must contain one run per side")
    if len(baseline_providers) != 1 or len(candidate_providers) != 1:
        raise ValueError("Comparison records must contain one provider per side")

    outcome_counts = Counter(record.outcome for record in records)
    baseline_counts = Counter(record.baseline_verdict for record in records)
    candidate_counts = Counter(record.candidate_verdict for record in records)

    return ComparisonSummary(
        comparison_id=(
            f"COMPARE-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-"
            f"{uuid4().hex[:8]}"
        ),
        baseline_run_id=next(iter(baseline_runs)),
        candidate_run_id=next(iter(candidate_runs)),
        baseline_provider=next(iter(baseline_providers)),
        candidate_provider=next(iter(candidate_providers)),
        test_pack_name=test_pack.test_pack.name,
        test_pack_version=test_pack.test_pack.version,
        total_comparisons=len(records),
        improved_count=outcome_counts[ComparisonOutcome.IMPROVED],
        regressed_count=outcome_counts[ComparisonOutcome.REGRESSED],
        unchanged_pass_count=outcome_counts[ComparisonOutcome.UNCHANGED_PASS],
        unchanged_issue_count=outcome_counts[ComparisonOutcome.UNCHANGED_ISSUE],
        indeterminate_count=outcome_counts[ComparisonOutcome.INDETERMINATE],
        baseline_pass_count=baseline_counts[EvaluationVerdict.PASS],
        baseline_fail_count=baseline_counts[EvaluationVerdict.FAIL],
        baseline_review_count=baseline_counts[EvaluationVerdict.REVIEW],
        baseline_error_count=baseline_counts[EvaluationVerdict.ERROR],
        candidate_pass_count=candidate_counts[EvaluationVerdict.PASS],
        candidate_fail_count=candidate_counts[EvaluationVerdict.FAIL],
        candidate_review_count=candidate_counts[EvaluationVerdict.REVIEW],
        candidate_error_count=candidate_counts[EvaluationVerdict.ERROR],
        generated_at=datetime.now(timezone.utc),
    )
