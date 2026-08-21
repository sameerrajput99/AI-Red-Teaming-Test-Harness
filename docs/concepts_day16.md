# Day 16 Concepts — Integration and End-to-End Testing

## Main Goal

Day 16 verifies that the components created through Day 15 work together as one complete system.

```text
YAML Test Pack
      ↓
Validation
      ↓
Provider Execution
      ↓
Security Evaluation
      ↓
Stability Analysis
      ↓
Risk Scoring
      ↓
Security Findings
      ↓
Assessment Report
      ↓
Sanitization
      ↓
Safe Artifacts + E2E Manifest
```

## Unit Test

A unit test verifies one isolated function or component.

Example: confirm that a stable critical failure receives risk score 100.

## Integration Test

An integration test verifies that connected components exchange compatible data and preserve expected meaning.

Example: stability output flows into risk scoring, and the resulting risk record flows into the finding builder.

## End-to-End Test

An end-to-end test starts from the same YAML input used by an operator and verifies the final safe artifacts.

Day 16 uses deterministic local providers so failures are repeatable and do not depend on network access, credentials, model availability, API cost, or changing LLM wording.

## Provider Matrix

| Provider | Expected result |
| --- | --- |
| `mock-vulnerable` | Stable security failures, non-zero risk, findings, critical posture |
| `mock-hardened` | Stable passes, zero risk, no findings |
| `mock-flaky` | Mixed results for prompt leakage, flaky status, uncertainty uplift |

## E2E Manifest

`e2e_manifest.json` records the counts produced by each stage and the final observed posture. It also explicitly records that raw prompts and raw responses were not exported.

The manifest supports traceability, but it is not a cryptographic attestation and does not prove complete AI security.

## Failure Scenarios Covered

- A stage returns the wrong number of records.
- Hardened behavior incorrectly creates a finding.
- Flaky behavior is incorrectly classified as stable.
- Expected artifacts are missing.
- In-memory counts and exported manifest counts disagree.
- Raw provider evidence leaks into the final assessment JSON.

## Memory Line

```text
Unit test = one component.
Integration test = connected components.
End-to-end test = complete input-to-output workflow.
```

## Limitation

Passing the deterministic Day 16 suite proves that the configured local workflow behaves as expected. It does not certify every model, prompt, evaluator, threat, or deployment environment as secure.
