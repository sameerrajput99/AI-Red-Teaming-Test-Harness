"""Execution engine for sending validated test cases to a chatbot provider."""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from .models import ExecutionRecord, ExecutionStatus, TestCase, TestPack
from .providers.base import ChatProvider
from .sanitization.engine import sanitize_text


MAX_PROVIDER_ERROR_DETAIL_CHARS = 500


def _safe_provider_error(error: Exception) -> str:
    """Return a bounded, redacted provider error suitable for stored evidence."""

    try:
        detail = " ".join(str(error).split())
    except Exception:  # noqa: BLE001 - exception formatting must not fail the run
        detail = "Provider execution failed."

    sanitized, _ = sanitize_text(detail)
    if not sanitized:
        sanitized = "Provider execution failed."

    bounded = sanitized[:MAX_PROVIDER_ERROR_DETAIL_CHARS]
    return f"{type(error).__name__}: {bounded}"


def execute_test_case(
    test_case: TestCase,
    provider: ChatProvider,
    run_id: str,
) -> ExecutionRecord:
    """Execute one validated test case and capture raw evidence."""

    started = perf_counter()

    try:
        provider_response = provider.generate(test_case.prompt)
        latency_ms = max(0, round((perf_counter() - started) * 1000))

        return ExecutionRecord(
            run_id=run_id,
            test_id=test_case.id,
            provider_name=provider.name,
            prompt=test_case.prompt,
            response=provider_response.text,
            execution_status=ExecutionStatus.SUCCESS,
            latency_ms=latency_ms,
            error_message=None,
            timestamp=datetime.now(timezone.utc),
        )
    except Exception as error:  # noqa: BLE001 - boundary converts provider failures to evidence
        latency_ms = max(0, round((perf_counter() - started) * 1000))

        return ExecutionRecord(
            run_id=run_id,
            test_id=test_case.id,
            provider_name=provider.name,
            prompt=test_case.prompt,
            response=None,
            execution_status=ExecutionStatus.ERROR,
            latency_ms=latency_ms,
            error_message=_safe_provider_error(error),
            timestamp=datetime.now(timezone.utc),
        )


def run_test_pack(test_pack: TestPack, provider: ChatProvider) -> list[ExecutionRecord]:
    """Execute every test case in a validated pack using one shared run ID."""

    run_id = f"RUN-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid4().hex[:8]}"
    records: list[ExecutionRecord] = []

    for test_case in test_pack.test_cases:
        for _ in range(test_case.repetitions):
            records.append(execute_test_case(test_case, provider, run_id))

    return records
