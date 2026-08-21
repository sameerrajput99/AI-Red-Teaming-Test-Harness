# Architecture Through Day 16

```text
Structured Test Pack
        ↓
Provider Execution
        ↓
Deterministic Evaluators
        ↓
Stability Analysis
        ↓
Risk Scoring
        ↓
Normalized Findings
        ↓
Assessment Builder
        ↓
Assessment Report (in memory)
        ↓
Sanitization Layer
        ├── API-key redaction
        ├── bearer-token redaction
        ├── generic secret redaction
        └── email redaction
        ↓
Sanitized Assessment Copy
        ↓
Safe Export
        ├── assessment_report.json
        ├── assessment_report.md
        ├── assessment_report.html
        └── sanitization_summary.json
        ↓
End-to-End Verification Manifest
        └── e2e_manifest.json
```

## Day 16 Orchestration Boundary

The `e2e` workflow invokes each existing production component once and preserves the intermediate typed results for integration assertions. It does not reimplement evaluator, stability, risk, finding, assessment, or sanitization rules.

The E2E manifest records stage counts, final observed posture, expected safe artifacts, and the raw-evidence export policy.

## Sanitization Boundary

The sanitization step occurs immediately before assessment artifacts are written.

This keeps report construction separate from export safety.

## Data Minimization

Day 13 findings already use a concise evidence summary rather than copying full provider responses into the normalized finding.

Day 15 preserves that design and adds deterministic redaction as another safety layer.

## Safe Export Metadata

`sanitization_summary.json` records which policy ran and how many configured redactions were made.

It also explicitly records:

```text
raw_response_exported = false
raw_prompt_exported = false
```

## Sanitization vs HTML Escaping

Sanitization protects sensitive content.

HTML escaping protects the static HTML renderer from interpreting untrusted report text as markup or script.

They are complementary controls.

## Limitation

Regex rules can only identify patterns they are designed to match.

Safe export therefore reduces exposure risk but does not replace manual report review or broader data-loss-prevention controls.
