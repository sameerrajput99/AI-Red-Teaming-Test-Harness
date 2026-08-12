"""Composite security-evaluation engine for raw execution evidence."""

from __future__ import annotations

from ..models import (
    EvaluatedRecord,
    EvaluationFinding,
    EvaluationVerdict,
    ExecutionRecord,
    ExecutionStatus,
    TestCase,
    TestPack,
)
from .factory import get_evaluator


def combine_findings(findings: list[EvaluationFinding]) -> EvaluationVerdict:
    """Combine findings conservatively using explicit verdict precedence."""

    if not findings:
        return EvaluationVerdict.REVIEW

    verdicts = {finding.verdict for finding in findings}
    if EvaluationVerdict.ERROR in verdicts:
        return EvaluationVerdict.ERROR
    if EvaluationVerdict.FAIL in verdicts:
        return EvaluationVerdict.FAIL
    if EvaluationVerdict.REVIEW in verdicts:
        return EvaluationVerdict.REVIEW
    return EvaluationVerdict.PASS


def _final_verdict(findings: list[EvaluationFinding]) -> EvaluationVerdict:
    """Backward-compatible wrapper around the Day 10 combiner."""

    return combine_findings(findings)


def evaluate_execution(
    test_case: TestCase,
    execution: ExecutionRecord,
) -> EvaluatedRecord:
    if execution.execution_status is ExecutionStatus.ERROR:
        finding = EvaluationFinding(
            evaluator_type="execution",
            verdict=EvaluationVerdict.ERROR,
            reason=execution.error_message or "The provider call failed.",
            matched_values=[],
        )
        return EvaluatedRecord(
            execution=execution,
            security_verdict=EvaluationVerdict.ERROR,
            findings=[finding],
            summary="The test could not be evaluated because execution failed.",
        )

    findings: list[EvaluationFinding] = []
    for config in test_case.evaluators:
        evaluator = get_evaluator(config.type)
        if evaluator is None:
            findings.append(
                EvaluationFinding(
                    evaluator_type=config.type,
                    verdict=EvaluationVerdict.REVIEW,
                    reason=(
                        f"Evaluator type '{config.type}' is not implemented; "
                        "human review is required."
                    ),
                    matched_values=[],
                )
            )
            continue

        findings.append(evaluator.evaluate(test_case, execution, config))

    verdict = combine_findings(findings)
    summary = {
        EvaluationVerdict.PASS: "All configured evaluators passed.",
        EvaluationVerdict.FAIL: "At least one evaluator detected a clear security failure.",
        EvaluationVerdict.REVIEW: "No clear failure was detected, but human review is required.",
        EvaluationVerdict.ERROR: "The evaluation could not be completed.",
    }[verdict]

    return EvaluatedRecord(
        execution=execution,
        security_verdict=verdict,
        findings=findings,
        summary=summary,
    )


def evaluate_test_pack(
    test_pack: TestPack,
    executions: list[ExecutionRecord],
) -> list[EvaluatedRecord]:
    cases_by_id = {case.id: case for case in test_pack.test_cases}
    evaluated: list[EvaluatedRecord] = []

    for execution in executions:
        test_case = cases_by_id.get(execution.test_id)
        if test_case is None:
            finding = EvaluationFinding(
                evaluator_type="test_case_lookup",
                verdict=EvaluationVerdict.ERROR,
                reason=f"No test definition was found for {execution.test_id}.",
                matched_values=[],
            )
            evaluated.append(
                EvaluatedRecord(
                    execution=execution,
                    security_verdict=EvaluationVerdict.ERROR,
                    findings=[finding],
                    summary="The execution could not be matched to a test definition.",
                )
            )
            continue

        evaluated.append(evaluate_execution(test_case, execution))

    return evaluated
