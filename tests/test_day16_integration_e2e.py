"""Day 16 integration and end-to-end regression tests."""

from __future__ import annotations

import json
from pathlib import Path

from ai_red_teaming_harness.assessment.models import AssessmentPosture
from ai_red_teaming_harness.e2e.workflow import ARTIFACT_NAMES, run_e2e_workflow
from ai_red_teaming_harness.risk.models import RiskLevel
from ai_red_teaming_harness.stability.models import StabilityStatus


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACK = PROJECT_ROOT / "test_packs" / "day12_risk_scoring_pack.yaml"


def test_vulnerable_pipeline_connects_all_stages(tmp_path: Path) -> None:
    result = run_e2e_workflow(PACK, "mock-vulnerable", tmp_path)

    assert len(result.executions) == 8
    assert len(result.evaluations) == 8
    assert len(result.stability_records) == 4
    assert len(result.risk_records) == 4
    assert result.findings_summary.total_findings == 3
    assert result.assessment.posture is AssessmentPosture.CRITICAL


def test_hardened_pipeline_has_no_observed_findings(tmp_path: Path) -> None:
    result = run_e2e_workflow(PACK, "mock-hardened", tmp_path)

    assert all(
        record.status is StabilityStatus.STABLE_PASS
        for record in result.stability_records
    )
    assert all(record.risk_level is RiskLevel.NONE for record in result.risk_records)
    assert result.findings == []
    assert result.assessment.posture is AssessmentPosture.NO_OBSERVED_FINDINGS


def test_flaky_pipeline_preserves_instability_for_prompt_leakage(
    tmp_path: Path,
) -> None:
    result = run_e2e_workflow(PACK, "mock-flaky", tmp_path)
    stability = {record.test_id: record for record in result.stability_records}
    risk = {record.test_id: record for record in result.risk_records}

    assert stability["RSK-001"].status is StabilityStatus.FLAKY
    assert stability["RSK-001"].pass_count == 1
    assert stability["RSK-001"].fail_count == 1
    assert risk["RSK-001"].risk_score == 70
    assert risk["RSK-001"].risk_level is RiskLevel.HIGH


def test_e2e_writes_complete_safe_artifact_set(tmp_path: Path) -> None:
    result = run_e2e_workflow(PACK, "mock-vulnerable", tmp_path)

    assert result.artifact_names == list(ARTIFACT_NAMES)
    assert all((result.output_dir / name).is_file() for name in ARTIFACT_NAMES)


def test_manifest_counts_match_in_memory_pipeline(tmp_path: Path) -> None:
    result = run_e2e_workflow(PACK, "mock-vulnerable", tmp_path)
    manifest = json.loads(
        (result.output_dir / "e2e_manifest.json").read_text(encoding="utf-8")
    )

    assert manifest["execution_count"] == len(result.executions)
    assert manifest["evaluation_count"] == len(result.evaluations)
    assert manifest["finding_count"] == len(result.findings)
    assert manifest["observed_posture"] == result.assessment.posture.value


def test_manifest_confirms_raw_evidence_is_not_exported(tmp_path: Path) -> None:
    result = run_e2e_workflow(PACK, "mock-vulnerable", tmp_path)
    manifest = json.loads(
        (result.output_dir / "e2e_manifest.json").read_text(encoding="utf-8")
    )

    assert manifest["raw_prompt_exported"] is False
    assert manifest["raw_response_exported"] is False


def test_exported_assessment_contains_no_raw_provider_response(
    tmp_path: Path,
) -> None:
    result = run_e2e_workflow(PACK, "mock-vulnerable", tmp_path)
    exported = (result.output_dir / "assessment_report.json").read_text(
        encoding="utf-8"
    )

    assert "SYSTEM_PROMPT:" not in exported
