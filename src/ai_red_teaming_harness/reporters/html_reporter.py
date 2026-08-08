"Human-readable HTML writer for one evaluated provider run."

from __future__ import annotations

from html import escape
from pathlib import Path

from ..models import EvaluatedRecord, RunSummary, TestPack
from .base import ReportWriter


def _safe(value: object | None) -> str:
    """Escape an untrusted value before placing it into HTML."""
    return escape("" if value is None else str(value), quote=True)


def _verdict_class(value: str) -> str:
    return {
        "PASS": "pass",
        "FAIL": "fail",
        "REVIEW": "review",
        "ERROR": "error",
    }.get(value, "neutral")


class HtmlReportWriter(ReportWriter):
    """Write a self-contained offline HTML evidence report."""

    @property
    def format_name(self) -> str:
        return "html"

    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[EvaluatedRecord],
        summary: RunSummary,
    ) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        cases_by_id = {case.id: case for case in test_pack.test_cases}

        record_sections: list[str] = []
        for record in records:
            execution = record.execution
            test_case = cases_by_id.get(execution.test_id)
            verdict = record.security_verdict.value
            findings = []
            for finding in record.findings:
                matches = ", ".join(_safe(value) for value in finding.matched_values)
                matched_html = (
                    f'<div class="matched"><strong>Matched:</strong> {matches}</div>'
                    if matches
                    else ""
                )
                findings.append(
                    f"""
                    <li>
                      <div class="finding-head">
                        <span>{_safe(finding.evaluator_type)}</span>
                        <span class="badge {_verdict_class(finding.verdict.value)}">
                          {_safe(finding.verdict.value)}
                        </span>
                      </div>
                      <p>{_safe(finding.reason)}</p>
                      {matched_html}
                    </li>
                    """
                )

            category = test_case.category.value if test_case else "unknown"
            severity = test_case.severity.value if test_case else "unknown"
            control_type = test_case.control_type.value if test_case else "unknown"
            title = test_case.title if test_case else execution.test_id

            record_sections.append(
                f"""
                <article class="record">
                  <header class="record-header">
                    <div>
                      <p class="eyebrow">{_safe(execution.test_id)} · {_safe(category)}</p>
                      <h2>{_safe(title)}</h2>
                    </div>
                    <span class="badge large {_verdict_class(verdict)}">{_safe(verdict)}</span>
                  </header>

                  <div class="metadata">
                    <span><strong>Severity:</strong> {_safe(severity)}</span>
                    <span><strong>Control:</strong> {_safe(control_type)}</span>
                    <span><strong>Execution:</strong> {_safe(execution.execution_status.value)}</span>
                    <span><strong>Latency:</strong> {_safe(execution.latency_ms)} ms</span>
                  </div>

                  <div class="evidence-grid">
                    <section>
                      <h3>Prompt</h3>
                      <pre>{_safe(execution.prompt)}</pre>
                    </section>
                    <section>
                      <h3>Response</h3>
                      <pre>{_safe(execution.response or execution.error_message or "")}</pre>
                    </section>
                  </div>

                  <details>
                    <summary>Evaluation findings</summary>
                    <p class="record-summary">{_safe(record.summary)}</p>
                    <ul class="findings">{''.join(findings)}</ul>
                  </details>
                </article>
                """
            )

        document = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Security-Policy"
        content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; script-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Red Teaming Run Report</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #08111f;
      --panel: #101c2e;
      --panel-2: #16243a;
      --text: #edf4ff;
      --muted: #9fb0c7;
      --line: #2b3c55;
      --pass: #39d98a;
      --fail: #ff6b7a;
      --review: #ffc857;
      --error: #c792ea;
      --accent: #63b3ff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, Segoe UI, Arial, sans-serif;
      line-height: 1.55;
    }}
    .container {{ width: min(1180px, calc(100% - 32px)); margin: 0 auto; padding: 44px 0 72px; }}
    .hero {{
      padding: 30px;
      border: 1px solid var(--line);
      border-radius: 20px;
      background: linear-gradient(145deg, var(--panel), #0c1728);
    }}
    h1, h2, h3, p {{ margin-top: 0; }}
    h1 {{ margin-bottom: 8px; font-size: clamp(2rem, 5vw, 3.4rem); }}
    .subtitle, .eyebrow {{ color: var(--muted); }}
    .eyebrow {{ margin-bottom: 6px; text-transform: uppercase; letter-spacing: .08em; font-size: .78rem; }}
    .meta-line {{ display: flex; flex-wrap: wrap; gap: 12px 24px; color: var(--muted); }}
    .cards {{ display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; margin: 20px 0 34px; }}
    .card {{ padding: 18px; border: 1px solid var(--line); border-radius: 15px; background: var(--panel); }}
    .card strong {{ display: block; font-size: 1.7rem; }}
    .card span {{ color: var(--muted); }}
    .record {{ margin-top: 18px; padding: 24px; border: 1px solid var(--line); border-radius: 18px; background: var(--panel); }}
    .record-header {{ display: flex; justify-content: space-between; gap: 18px; align-items: flex-start; }}
    .record-header h2 {{ margin-bottom: 0; }}
    .metadata {{ display: flex; flex-wrap: wrap; gap: 10px 18px; margin: 18px 0; color: var(--muted); }}
    .evidence-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    .evidence-grid section {{ min-width: 0; }}
    pre {{
      margin: 0;
      min-height: 110px;
      padding: 16px;
      overflow: auto;
      white-space: pre-wrap;
      overflow-wrap: anywhere;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #07101d;
      color: #dce9fa;
      font: 0.9rem/1.55 Consolas, monospace;
    }}
    details {{ margin-top: 16px; border-top: 1px solid var(--line); padding-top: 14px; }}
    summary {{ cursor: pointer; color: var(--accent); font-weight: 700; }}
    .findings {{ padding-left: 0; list-style: none; }}
    .findings li {{ margin-top: 10px; padding: 14px; border-radius: 12px; background: var(--panel-2); }}
    .finding-head {{ display: flex; justify-content: space-between; gap: 10px; font-weight: 700; }}
    .matched {{ color: var(--review); font-size: .92rem; }}
    .record-summary {{ color: var(--muted); margin-top: 12px; }}
    .badge {{ display: inline-flex; align-items: center; border-radius: 999px; padding: 4px 10px; font-weight: 800; font-size: .75rem; }}
    .badge.large {{ padding: 8px 14px; font-size: .86rem; }}
    .pass {{ color: var(--pass); background: rgba(57,217,138,.12); }}
    .fail {{ color: var(--fail); background: rgba(255,107,122,.12); }}
    .review {{ color: var(--review); background: rgba(255,200,87,.12); }}
    .error {{ color: var(--error); background: rgba(199,146,234,.12); }}
    .neutral {{ color: var(--muted); background: rgba(159,176,199,.12); }}
    .notice {{ margin-top: 28px; color: var(--muted); font-size: .9rem; }}
    @media (max-width: 850px) {{
      .cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .evidence-grid {{ grid-template-columns: 1fr; }}
    }}
    @media (max-width: 520px) {{
      .cards {{ grid-template-columns: 1fr; }}
      .record-header {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <main class="container">
    <section class="hero">
      <p class="eyebrow">AI Red Teaming Test Harness</p>
      <h1>Run Evidence Report</h1>
      <p class="subtitle">{_safe(test_pack.test_pack.name)} · version {_safe(test_pack.test_pack.version)}</p>
      <div class="meta-line">
        <span><strong>Run ID:</strong> {_safe(summary.run_id)}</span>
        <span><strong>Provider:</strong> {_safe(summary.provider_name)}</span>
        <span><strong>Generated:</strong> {_safe(summary.generated_at.isoformat())}</span>
      </div>
    </section>

    <section class="cards" aria-label="Run summary">
      <div class="card"><strong>{summary.total_tests}</strong><span>Total tests</span></div>
      <div class="card"><strong>{summary.pass_count}</strong><span>PASS</span></div>
      <div class="card"><strong>{summary.fail_count}</strong><span>FAIL</span></div>
      <div class="card"><strong>{summary.review_count}</strong><span>REVIEW</span></div>
      <div class="card"><strong>{summary.error_count}</strong><span>ERROR</span></div>
    </section>

    <section aria-label="Detailed test evidence">
      {''.join(record_sections)}
    </section>

    <p class="notice">
      This report applies only to the configured tests and evaluators. It is not a complete security certification.
    </p>
  </main>
</body>
</html>
"""
        destination.write_text(document, encoding="utf-8")
        return destination
