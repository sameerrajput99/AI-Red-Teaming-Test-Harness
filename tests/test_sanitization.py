"""Tests for Day 15 evidence sanitization and safe export."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ai_red_teaming_harness.assessment.builder import build_assessment_report
from ai_red_teaming_harness.assessment.reporter import write_assessment_reports
from ai_red_teaming_harness.findings.models import (
    FindingStatus,
    FindingsRunSummary,
    SecurityFinding,
)
from ai_red_teaming_harness.models import Category, ControlType, Severity
from ai_red_teaming_harness.risk.models import RiskLevel
from ai_red_teaming_harness.sanitization.engine import (
    sanitize_assessment_report,
    sanitize_text,
)
from ai_red_teaming_harness.stability.models import StabilityStatus


def _summary() -> FindingsRunSummary:
    return FindingsRunSummary(
        provider_name="mock-safe-export",
        test_pack_name="Day 15 Safe Export Pack",
        total_tests_assessed=1,
        total_findings=1,
        low_count=0,
        medium_count=0,
        high_count=1,
        critical_count=0,
        high_or_critical_count=1,
        highest_risk_score=75,
        generated_at=datetime.now(timezone.utc),
    )


def _finding(
    observation: str = "Sensitive evidence was observed during the configured test.",
    title: str = "Synthetic safe export finding",
) -> SecurityFinding:
    return SecurityFinding(
        finding_id="FND-TST-001",
        test_id="TST-001",
        title=title,
        provider_name="mock-safe-export",
        category=Category.SAFETY_BOUNDARY,
        control_type=ControlType.ADVERSARIAL,
        severity=Severity.HIGH,
        risk_score=75,
        risk_level=RiskLevel.HIGH,
        stability_status=StabilityStatus.STABLE_FAIL,
        pass_rate_percent=0.0,
        observed_issue_factor_percent=100.0,
        status=FindingStatus.OPEN,
        observation=observation,
        impact="Sensitive data exposure could create a security issue in a real system.",
        recommendation="Keep credentials outside model-visible content and rotate exposed credentials.",
        evidence_summary="Issue factor 100%; pass rate 0%; stability STABLE_FAIL.",
        created_at=datetime.now(timezone.utc),
    )


def test_sanitize_text_redacts_supported_sensitive_patterns() -> None:
    text = (
        "Contact analyst@example.com. "
        "API_KEY=DEMOSECRET123. "
        "Use Bearer abcdefghijklmnop. "
        "OpenAI key sk-abcdefghijklmnop."
    )

    sanitized, counts = sanitize_text(text)

    assert "analyst@example.com" not in sanitized
    assert "DEMOSECRET123" not in sanitized
    assert "abcdefghijklmnop" not in sanitized
    assert "[REDACTED_EMAIL]" in sanitized
    assert sum(counts.values()) == 4


def test_sanitize_assessment_report_returns_safe_copy_and_metadata() -> None:
    finding = _finding(
        observation=(
            "Observed API_KEY=TOPSECRET123 and contact security@example.com."
        )
    )
    report = build_assessment_report([finding], _summary())

    safe_report, summary = sanitize_assessment_report(report)

    assert "TOPSECRET123" not in safe_report.findings[0].observation
    assert "security@example.com" not in safe_report.findings[0].observation
    assert summary.total_redactions == 2
    assert summary.raw_response_exported is False
    assert summary.raw_prompt_exported is False


def test_safe_reporter_writes_four_artifacts(tmp_path: Path) -> None:
    report = build_assessment_report([_finding()], _summary())

    write_assessment_reports(tmp_path, report)

    assert (tmp_path / "assessment_report.json").is_file()
    assert (tmp_path / "assessment_report.md").is_file()
    assert (tmp_path / "assessment_report.html").is_file()
    assert (tmp_path / "sanitization_summary.json").is_file()


def test_raw_secret_does_not_appear_in_exported_reports(tmp_path: Path) -> None:
    secret = "ULTRASECRET999"
    finding = _finding(
        observation=f"Observed password={secret} during the test."
    )
    report = build_assessment_report([finding], _summary())

    write_assessment_reports(tmp_path, report)

    for name in (
        "assessment_report.json",
        "assessment_report.md",
        "assessment_report.html",
    ):
        exported = (tmp_path / name).read_text(encoding="utf-8")
        assert secret not in exported
        assert "[REDACTED_SECRET]" in exported


def test_html_escaping_still_applies_after_sanitization(tmp_path: Path) -> None:
    finding = _finding(
        title="Finding <script>alert(1)</script>",
        observation="Contact analyst@example.com for the raw evidence.",
    )
    report = build_assessment_report([finding], _summary())

    write_assessment_reports(tmp_path, report)
    html = (tmp_path / "assessment_report.html").read_text(encoding="utf-8")

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "analyst@example.com" not in html


def test_clean_report_requires_zero_redactions() -> None:
    report = build_assessment_report([_finding()], _summary())

    _, summary = sanitize_assessment_report(report)

    assert summary.total_redactions == 0
    assert summary.redactions_by_rule == {}
