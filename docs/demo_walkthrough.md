# Demo Walkthrough

## Purpose

This walkthrough presents the AI Red Teaming Test Harness as a repeatable
engineering project rather than a collection of disconnected scripts.

The included demo uses deterministic local providers. It does not require an
API key and does not claim production-model security.

## Before the Demo

From the project root:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
```

Expected verified regression baseline:

```text
120 passed
```

## One-Command Showcase

Run:

```powershell
showcase-ai-security
```

The command performs five stages:

```text
Vulnerable baseline E2E assessment
                ↓
Hardened candidate E2E assessment
                ↓
Test-level verdict comparison
                ↓
Strict security policy gate
                ↓
Safe showcase export
```

Expected deterministic result:

| Measure | Expected |
| --- | ---: |
| Test scenarios | 5 |
| Improved | 4 |
| Regressed | 0 |
| Unchanged pass | 1 |
| Candidate failures | 0 |
| Policy gate | `PASSED` |

![Verified deterministic showcase result](assets/day18_showcase_result.svg)

## What to Open

The command prints the timestamped output location. Open:

```text
output/SHOWCASE-.../showcase_summary.md
```

Explain that it contains aggregate postures, finding counts, test verdicts,
comparison outcomes, and the policy-gate result.

Then open:

```text
output/SHOWCASE-.../showcase_manifest.json
```

Point out:

```json
"raw_prompt_exported": false,
"raw_response_exported": false
```

These flags describe the top-level showcase export. Every artifact must still
be reviewed before external sharing.

## 30-Second Explanation

> This project converts structured YAML security scenarios into repeatable AI
> assessments. The showcase runs the same five tests against a deterministic
> vulnerable baseline and hardened candidate. It detects four improvements,
> preserves the benign control, finds no regression, and applies an explicit
> policy gate. The final showcase files contain scope-limited aggregate evidence
> rather than raw attack prompts or responses.

## Two-Minute Technical Walkthrough

1. The YAML pack defines attack category, severity, expected behavior, and
   deterministic evaluator rules.
2. Provider adapters execute the same pack against vulnerable and hardened
   configurations.
3. Evaluators convert response evidence into `PASS`, `FAIL`, `REVIEW`, or
   `ERROR` verdicts.
4. Stability, risk, findings, assessment, and sanitization stages build each
   complete E2E result.
5. The comparison engine classifies every pair as improved, regressed,
   unchanged, or indeterminate.
6. The policy gate enforces explicit acceptance thresholds.
7. The showcase exports a concise human summary and machine-readable manifest.

## Safe Demo Rules

- Use only the included mock providers during a public demonstration.
- Do not display `.env`, local API keys, raw provider diagnostics, or private
  output folders.
- Do not call the result a penetration-test certificate.
- Say `NO_OBSERVED_FINDINGS within the configured scope`, not `fully secure`.
- Keep personal filesystem paths out of screenshots before publishing them.
