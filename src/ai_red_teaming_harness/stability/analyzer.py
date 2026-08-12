"""Aggregate evaluated repetitions into pass-rate and flakiness metrics."""

from __future__ import annotations

from collections import defaultdict

from ..models import EvaluatedRecord, EvaluationVerdict, TestPack
from .models import StabilityRecord, StabilityRunSummary, StabilityStatus


_STATUS_BY_SINGLE_VERDICT = {
    EvaluationVerdict.PASS: StabilityStatus.STABLE_PASS,
    EvaluationVerdict.FAIL: StabilityStatus.STABLE_FAIL,
    EvaluationVerdict.REVIEW: StabilityStatus.STABLE_REVIEW,
    EvaluationVerdict.ERROR: StabilityStatus.STABLE_ERROR,
}


def _status_for(verdicts: list[EvaluationVerdict]) -> StabilityStatus:
    unique = set(verdicts)
    if len(unique) > 1:
        return StabilityStatus.FLAKY
    return _STATUS_BY_SINGLE_VERDICT[verdicts[0]]


def analyze_stability(
    test_pack: TestPack,
    evaluated_records: list[EvaluatedRecord],
) -> tuple[list[StabilityRecord], StabilityRunSummary]:
    """Compute repeated-run metrics for every test definition in the pack."""

    grouped: dict[str, list[EvaluatedRecord]] = defaultdict(list)
    for record in evaluated_records:
        grouped[record.execution.test_id].append(record)

    stability_records: list[StabilityRecord] = []

    for test_case in test_pack.test_cases:
        records = grouped.get(test_case.id, [])
        if not records:
            continue

        verdicts = [record.security_verdict for record in records]
        pass_count = verdicts.count(EvaluationVerdict.PASS)
        fail_count = verdicts.count(EvaluationVerdict.FAIL)
        review_count = verdicts.count(EvaluationVerdict.REVIEW)
        error_count = verdicts.count(EvaluationVerdict.ERROR)
        total_attempts = len(verdicts)
        pass_rate = round((pass_count / total_attempts) * 100, 2)

        seen = [
            verdict
            for verdict in (
                EvaluationVerdict.PASS,
                EvaluationVerdict.FAIL,
                EvaluationVerdict.REVIEW,
                EvaluationVerdict.ERROR,
            )
            if verdict in verdicts
        ]

        stability_records.append(
            StabilityRecord(
                test_id=test_case.id,
                title=test_case.title,
                category=test_case.category,
                control_type=test_case.control_type,
                severity=test_case.severity,
                total_attempts=total_attempts,
                pass_count=pass_count,
                fail_count=fail_count,
                review_count=review_count,
                error_count=error_count,
                pass_rate_percent=pass_rate,
                verdicts_seen=seen,
                status=_status_for(verdicts),
            )
        )

    if not stability_records:
        raise ValueError("No evaluated records were available for stability analysis.")

    stable_pass_count = sum(
        record.status is StabilityStatus.STABLE_PASS
        for record in stability_records
    )
    flaky_count = sum(
        record.status is StabilityStatus.FLAKY
        for record in stability_records
    )
    stable_issue_count = (
        len(stability_records) - stable_pass_count - flaky_count
    )

    provider_name = evaluated_records[0].execution.provider_name
    total_attempts = sum(record.total_attempts for record in stability_records)
    average_pass_rate = round(
        sum(record.pass_rate_percent for record in stability_records)
        / len(stability_records),
        2,
    )

    summary = StabilityRunSummary(
        provider_name=provider_name,
        test_pack_name=test_pack.test_pack.name,
        total_tests=len(stability_records),
        total_attempts=total_attempts,
        stable_pass_count=stable_pass_count,
        stable_issue_count=stable_issue_count,
        flaky_count=flaky_count,
        average_pass_rate_percent=average_pass_rate,
    )

    return stability_records, summary
