"Human-readable HTML writer for baseline-versus-candidate comparisons."

from __future__ import annotations

from html import escape
from pathlib import Path

from ..models import ComparisonRecord, ComparisonSummary, TestPack


def _safe(value: object | None) -> str:
    """Escape an untrusted value before placing it into HTML."""
    return escape("" if value is None else str(value), quote=True)


def _outcome_class(value: str) -> str:
    return {
        "IMPROVED": "improved",
        "REGRESSED": "regressed",
        "UNCHANGED_PASS": "unchanged-pass",
        "UNCHANGED_ISSUE": "unchanged-issue",
        "INDETERMINATE": "indeterminate",
    }.get(value, "neutral")


def _verdict_class(value: str) -> str:
    return {
        "PASS": "pass",
        "FAIL": "fail",
        "REVIEW": "review",
        "ERROR": "error",
    }.get(value, "neutral")


class ComparisonHtmlWriter:
    """Write a self-contained offline HTML comparison report."""

    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[ComparisonRecord],
        summary: ComparisonSummary,
    ) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)

        record_sections: list[str] = []
        for record in records:
            record_sections.append(
                f"""
                <article class="record">
                  <header class="record-header">
                    <div>
                      <p class="eyebrow">{_safe(record.test_id)} · attempt {_safe(record.attempt)}</p>
                      <h2>{_safe(record.title)}</h2>
                    </div>
                    <span class="badge large {_outcome_class(record.outcome.value)}">
                      {_safe(record.outcome.value)}
                    </span>
                  </header>

                  <div class="metadata">
                    <span><strong>Category:</strong> {_safe(record.category.value)}</span>
                    <span><strong>Severity:</strong> {_safe(record.severity.value)}</span>
                    <span><strong>Control:</strong> {_safe(record.control_type.value)}</span>
                  </div>

                  <div class="comparison-grid">
                    <section>
                      <div class="side-title">
                        <h3>Baseline</h3>
                        <span class="badge {_verdict_class(record.baseline_verdict.value)}">
                          {_safe(record.baseline_verdict.value)}
                        </span>
                      </div>
                      <p class="provider">{_safe(record.baseline_provider)}</p>
                      <pre>{_safe(record.baseline_response or "")}</pre>
                    </section>

                    <section>
                      <div class="side-title">
                        <h3>Candidate</h3>
                        <span class="badge {_verdict_class(record.candidate_verdict.value)}">
                          {_safe(record.candidate_verdict.value)}
                        </span>
                      </div>
                      <p class="provider">{_safe(record.candidate_provider)}</p>
                      <pre>{_safe(record.candidate_response or "")}</pre>
                    </section>
                  </div>

                  <p class="explanation">{_safe(record.explanation)}</p>
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
  <title>AI Red Teaming Comparison Report</title>
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
    .subtitle, .eyebrow, .provider {{ color: var(--muted); }}
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
    .comparison-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
    .comparison-grid section {{ min-width: 0; padding: 16px; border: 1px solid var(--line); border-radius: 14px; background: var(--panel-2); }}
    .side-title {{ display: flex; justify-content: space-between; gap: 12px; }}
    .side-title h3, .provider {{ margin-bottom: 8px; }}
    pre {{
      margin: 0;
      min-height: 130px;
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
    .explanation {{ margin: 16px 0 0; padding: 14px; border-left: 3px solid var(--accent); background: rgba(99,179,255,.08); }}
    .badge {{ display: inline-flex; align-items: center; border-radius: 999px; padding: 4px 10px; font-weight: 800; font-size: .75rem; }}
    .badge.large {{ padding: 8px 14px; font-size: .86rem; }}
    .pass, .improved, .unchanged-pass {{ color: var(--pass); background: rgba(57,217,138,.12); }}
    .fail, .regressed {{ color: var(--fail); background: rgba(255,107,122,.12); }}
    .review, .unchanged-issue {{ color: var(--review); background: rgba(255,200,87,.12); }}
    .error, .indeterminate {{ color: var(--error); background: rgba(199,146,234,.12); }}
    .neutral {{ color: var(--muted); background: rgba(159,176,199,.12); }}
    .notice {{ margin-top: 28px; color: var(--muted); font-size: .9rem; }}
    @media (max-width: 850px) {{
      .cards {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .comparison-grid {{ grid-template-columns: 1fr; }}
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
      <h1>Baseline vs Candidate</h1>
      <p class="subtitle">{_safe(test_pack.test_pack.name)} · version {_safe(test_pack.test_pack.version)}</p>
      <div class="meta-line">
        <span><strong>Comparison ID:</strong> {_safe(summary.comparison_id)}</span>
        <span><strong>Baseline:</strong> {_safe(summary.baseline_provider)}</span>
        <span><strong>Candidate:</strong> {_safe(summary.candidate_provider)}</span>
        <span><strong>Generated:</strong> {_safe(summary.generated_at.isoformat())}</span>
      </div>
    </section>

    <section class="cards" aria-label="Comparison summary">
      <div class="card"><strong>{summary.total_comparisons}</strong><span>Total comparisons</span></div>
      <div class="card"><strong>{summary.improved_count}</strong><span>IMPROVED</span></div>
      <div class="card"><strong>{summary.regressed_count}</strong><span>REGRESSED</span></div>
      <div class="card"><strong>{summary.unchanged_pass_count}</strong><span>UNCHANGED PASS</span></div>
      <div class="card"><strong>{summary.indeterminate_count}</strong><span>INDETERMINATE</span></div>
    </section>

    <section aria-label="Detailed comparison evidence">
      {''.join(record_sections)}
    </section>

    <p class="notice">
      Improvements apply only to the configured tests and evaluators. This report is not a complete security certification.
    </p>
  </main>
</body>
</html>
"""
        destination.write_text(document, encoding="utf-8")
        return destination
