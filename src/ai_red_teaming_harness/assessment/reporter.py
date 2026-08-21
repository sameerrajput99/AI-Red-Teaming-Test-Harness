"""Sanitized JSON, Markdown and safe static HTML reporters for assessments."""

from __future__ import annotations

from html import escape
import json
from pathlib import Path

from .models import AssessmentReport
from ..sanitization.engine import sanitize_assessment_report


def _markdown(report: AssessmentReport) -> str:
    lines = [
        f"# {report.title}",
        "",
        f"- Report ID: `{report.report_id}`",
        f"- Provider: `{report.provider_name}`",
        f"- Test Pack: `{report.test_pack_name}`",
        f"- Observed Posture: **{report.posture.value}**",
        f"- Generated At: `{report.generated_at.isoformat()}`",
        "",
        "## Executive Summary",
        "",
        report.executive_summary,
        "",
        "## Scope",
        "",
        report.scope_statement,
        "",
        "## Key Metrics",
        "",
        f"- Tests assessed: {report.findings_summary.total_tests_assessed}",
        f"- Total findings: {report.findings_summary.total_findings}",
        f"- Critical findings: {report.findings_summary.critical_count}",
        f"- High findings: {report.findings_summary.high_count}",
        f"- Medium findings: {report.findings_summary.medium_count}",
        f"- Low findings: {report.findings_summary.low_count}",
        f"- Highest risk score: {report.findings_summary.highest_risk_score}/100",
        "",
        "## Findings",
        "",
    ]

    if not report.findings:
        lines.extend([
            "No normalized non-zero security findings were observed in this configured assessment.",
            "",
        ])
    else:
        for finding in report.findings:
            lines.extend([
                f"### {finding.finding_id} — {finding.title}",
                "",
                f"- Test ID: `{finding.test_id}`",
                f"- Severity: **{finding.severity.value.upper()}**",
                f"- Risk: **{finding.risk_score}/100 ({finding.risk_level.value})**",
                f"- Stability: `{finding.stability_status.value}`",
                f"- Status: `{finding.status.value}`",
                "",
                f"**Observation:** {finding.observation}",
                "",
                f"**Impact:** {finding.impact}",
                "",
                f"**Recommendation:** {finding.recommendation}",
                "",
                f"**Evidence Summary:** {finding.evidence_summary}",
                "",
            ])

    lines.extend(["## Prioritized Actions", ""])
    if report.prioritized_actions:
        for index, action in enumerate(report.prioritized_actions, start=1):
            lines.append(f"{index}. {action}")
    else:
        lines.append(
            "No remediation action is generated because no normalized "
            "non-zero finding was observed."
        )

    lines.extend(["", "## Methodology", ""])
    for step in report.methodology:
        lines.append(f"- {step}")

    lines.extend(["", "## Limitations", ""])
    for limitation in report.limitations:
        lines.append(f"- {limitation}")

    lines.append("")
    return "\n".join(lines)


def _html(report: AssessmentReport) -> str:
    finding_cards = []
    for finding in report.findings:
        finding_cards.append(
            f"""
            <section class="finding">
              <h3>{escape(finding.finding_id)} — {escape(finding.title)}</h3>
              <p><strong>Test:</strong> {escape(finding.test_id)}</p>
              <p><strong>Severity:</strong> {escape(finding.severity.value.upper())}</p>
              <p><strong>Risk:</strong> {finding.risk_score}/100 ({escape(finding.risk_level.value)})</p>
              <p><strong>Stability:</strong> {escape(finding.stability_status.value)}</p>
              <p><strong>Status:</strong> {escape(finding.status.value)}</p>
              <h4>Observation</h4>
              <p>{escape(finding.observation)}</p>
              <h4>Impact</h4>
              <p>{escape(finding.impact)}</p>
              <h4>Recommendation</h4>
              <p>{escape(finding.recommendation)}</p>
              <h4>Evidence Summary</h4>
              <p>{escape(finding.evidence_summary)}</p>
            </section>
            """
        )

    findings_html = "\n".join(finding_cards)
    if not findings_html:
        findings_html = (
            "<p>No normalized non-zero security findings were observed in this "
            "configured assessment.</p>"
        )

    actions_html = "".join(
        f"<li>{escape(action)}</li>" for action in report.prioritized_actions
    )
    if not actions_html:
        actions_html = (
            "<li>No remediation action is generated because no normalized "
            "non-zero finding was observed.</li>"
        )

    methodology_html = "".join(
        f"<li>{escape(step)}</li>" for step in report.methodology
    )
    limitations_html = "".join(
        f"<li>{escape(item)}</li>" for item in report.limitations
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:;">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(report.title)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 1000px; margin: 40px auto; padding: 0 24px; line-height: 1.55; }}
    header, section {{ margin-bottom: 28px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; }}
    .metric, .finding {{ border: 1px solid #bbb; border-radius: 8px; padding: 16px; }}
    .posture {{ font-size: 1.15rem; font-weight: 700; }}
    code {{ word-break: break-word; }}
  </style>
</head>
<body>
  <header>
    <h1>{escape(report.title)}</h1>
    <p><strong>Report ID:</strong> {escape(report.report_id)}</p>
    <p><strong>Provider:</strong> {escape(report.provider_name)}</p>
    <p><strong>Test Pack:</strong> {escape(report.test_pack_name)}</p>
    <p class="posture"><strong>Observed Posture:</strong> {escape(report.posture.value)}</p>
    <p><strong>Generated At:</strong> {escape(report.generated_at.isoformat())}</p>
  </header>

  <section>
    <h2>Executive Summary</h2>
    <p>{escape(report.executive_summary)}</p>
  </section>

  <section>
    <h2>Scope</h2>
    <p>{escape(report.scope_statement)}</p>
  </section>

  <section>
    <h2>Key Metrics</h2>
    <div class="metrics">
      <div class="metric"><strong>Tests</strong><br>{report.findings_summary.total_tests_assessed}</div>
      <div class="metric"><strong>Findings</strong><br>{report.findings_summary.total_findings}</div>
      <div class="metric"><strong>Critical</strong><br>{report.findings_summary.critical_count}</div>
      <div class="metric"><strong>High</strong><br>{report.findings_summary.high_count}</div>
      <div class="metric"><strong>Highest Risk</strong><br>{report.findings_summary.highest_risk_score}/100</div>
    </div>
  </section>

  <section>
    <h2>Findings</h2>
    {findings_html}
  </section>

  <section>
    <h2>Prioritized Actions</h2>
    <ol>{actions_html}</ol>
  </section>

  <section>
    <h2>Methodology</h2>
    <ul>{methodology_html}</ul>
  </section>

  <section>
    <h2>Limitations</h2>
    <ul>{limitations_html}</ul>
  </section>
</body>
</html>
"""


def write_assessment_reports(
    output_dir: Path,
    report: AssessmentReport,
) -> None:
    """Sanitize the report first, then export only the sanitized copy."""

    output_dir.mkdir(parents=True, exist_ok=True)

    safe_report, sanitization_summary = sanitize_assessment_report(
        report
    )

    (output_dir / "assessment_report.json").write_text(
        json.dumps(safe_report.model_dump(mode="json"), indent=2),
        encoding="utf-8",
    )
    (output_dir / "assessment_report.md").write_text(
        _markdown(safe_report),
        encoding="utf-8",
    )
    (output_dir / "assessment_report.html").write_text(
        _html(safe_report),
        encoding="utf-8",
    )
    (output_dir / "sanitization_summary.json").write_text(
        json.dumps(
            sanitization_summary.model_dump(mode="json"),
            indent=2,
        ),
        encoding="utf-8",
    )
