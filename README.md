# AI Red Teaming Test Harness

A safe, reproducible Python framework for structured AI red teaming tests, deterministic evaluation, stability analysis, risk prioritization, normalized findings, consolidated assessment reporting, and sanitized safe export.

## Current Status: Day 16

Day 16 adds **Integration & End-to-End Testing** across the complete local assessment pipeline.

The new command is:

```powershell
e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-vulnerable
```

It connects validation, provider execution, evaluation, stability analysis, risk scoring, finding generation, assessment reporting, and sanitization in one observable workflow.

The final output now includes:

```text
assessment_report.json
assessment_report.md
assessment_report.html
sanitization_summary.json
e2e_manifest.json
```

The Day 16 regression baseline is:

```text
92 passed
```

## Day 15 Foundation

Day 15 added **Evidence Sanitization & Safe Export**.

The key idea is:

```text
Assessment Report
      ↓
Sanitization Layer
      ↓
Safe Export
```

The project now redacts configured sensitive-text patterns before JSON, Markdown, or HTML assessment artifacts are written.

## Why Sanitization Matters

Security evidence can accidentally contain:

```text
API keys
Bearer tokens
generic secrets/passwords/tokens
email addresses
```

A report should not make sensitive evidence easier to leak.

Day 15 therefore applies a deterministic redaction policy before export.

## Default Redaction Examples

```text
sk-abcdefghijklmnop
→ [REDACTED_API_KEY]

Bearer abcdefghijklmnop
→ Bearer [REDACTED_TOKEN]

API_KEY=DEMOSECRET123
→ API_KEY=[REDACTED_SECRET]

analyst@example.com
→ [REDACTED_EMAIL]
```

## Important Design Choice

The final assessment exporter writes only the **sanitized copy**.

The in-memory assessment model can still contain the original structured content during local processing, but exported assessment files are produced from the sanitized version.

## Safe Export Artifacts

`assessment-ai-tests` still creates:

```text
assessment_report.json
assessment_report.md
assessment_report.html
```

Day 15 also adds:

```text
sanitization_summary.json
```

The sanitization summary records:

```text
policy_name
total_redactions
redactions_by_rule
raw_response_exported = false
raw_prompt_exported = false
```

## Data Minimization

The final assessment report does not export complete raw prompts or raw provider responses.

Instead, findings use concise evidence summaries such as:

```text
issue factor
pass rate
stability
severity
```

This reduces unnecessary sensitive-data exposure.

## Sanitization vs HTML Escaping

They solve different problems.

### Sanitization

Removes configured sensitive data.

### HTML Escaping

Stops report text from becoming executable HTML/script content.

Both are applied in the final export path.

## Run Day 15

Day 15 does not add a new CLI command.

Use the existing assessment command:

```powershell
assessment-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-vulnerable
```

Then inspect the generated assessment folder.

## Regression Tests

```powershell
python -m pytest
```

Expected after Day 15:

```text
85 passed
```

## Important Limitation

Regex-based sanitization is defense-in-depth, not a perfect secret-detection system.

A sensitive value that does not match the configured policy can still be missed.

Always review reports before external sharing.
