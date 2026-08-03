"""Run-level summary calculations for evaluated test evidence."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone

from ..models import EvaluatedRecord, EvaluationVerdict, RunSummary, TestPack


def build_run_summary(test_pack: TestPack, records: list[EvaluatedRecord]) -> RunSummary:
    """Create one validated summary from evaluated records."""

    if not records:
        raise ValueError("Cannot summarize an empty evaluated-record list")

    run_ids = {record.execution.run_id for record in records}
    providers = {record.execution.provider_name for record in records}
    if len(run_ids) != 1:
        raise ValueError("All evaluated records must belong to one run_id")
    if len(providers) != 1:
        raise ValueError("All evaluated records must belong to one provider")

    counts = Counter(record.security_verdict for record in records)
    average_latency = round(
        sum(record.execution.latency_ms for record in records) / len(records),
        2,
    )

    return RunSummary(
        run_id=next(iter(run_ids)),
        provider_name=next(iter(providers)),
        test_pack_name=test_pack.test_pack.name,
        test_pack_version=test_pack.test_pack.version,
        total_tests=len(records),
        pass_count=counts[EvaluationVerdict.PASS],
        fail_count=counts[EvaluationVerdict.FAIL],
        review_count=counts[EvaluationVerdict.REVIEW],
        error_count=counts[EvaluationVerdict.ERROR],
        average_latency_ms=average_latency,
        generated_at=datetime.now(timezone.utc),
    )
