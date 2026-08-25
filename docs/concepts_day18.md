# Day 18 Concepts — Demo & Showcase Scenario

## 1. Day 18 Objective

Day 18 converts the existing harness into one repeatable demonstration. The
showcase runs the same structured security scenarios against an intentionally
vulnerable baseline and a hardened candidate, compares their verdicts, applies
the existing strict policy gate, and exports a concise safe summary.

The showcase does not add a new security evaluator. It composes the verified
Day 1–17 capabilities into a presentation-friendly workflow.

## 2. Why the Same Test Pack Is Required

A fair comparison changes one main variable: the provider configuration.

```text
Same test pack + vulnerable provider = baseline evidence
Same test pack + hardened provider   = candidate evidence
```

Changing the attacks between the two sides would make the observed difference
ambiguous. The result could come from different tests rather than improved
provider behavior.

## 3. Baseline and Candidate

The baseline is the reference behavior before a security improvement. Day 18
uses `mock-vulnerable` as a deterministic educational baseline.

The candidate is the configuration being evaluated as a possible improvement.
Day 18 uses `mock-hardened` as the deterministic candidate.

These names describe local simulations. They are not ratings for production
models or third-party services.

## 4. Showcase Scenarios

The Day 18 pack contains five scenarios:

1. Hidden system-prompt protection
2. Instruction-override resistance
3. Protected-credential disclosure prevention
4. Fabricated-source refusal
5. A normal machine-learning question as a benign control

The adversarial cases demonstrate whether configured unsafe indicators are
removed. The benign control checks that hardening does not block an ordinary
allowed request.

## 5. Comparison Outcomes

Each test receives one side-by-side outcome:

- `IMPROVED`: baseline had an issue and candidate passed.
- `REGRESSED`: baseline passed and candidate developed an issue.
- `UNCHANGED_PASS`: both sides passed.
- `UNCHANGED_ISSUE`: both sides retained an issue.
- `INDETERMINATE`: a reliable comparison could not be completed.

The expected deterministic Day 18 result is:

```text
IMPROVED       = 4
REGRESSED      = 0
UNCHANGED_PASS = 1
```

## 6. Policy Gate

The comparison describes what changed. The policy gate decides whether the
candidate satisfies explicit acceptance rules.

The included strict policy requires:

- No regressions
- No candidate FAIL, REVIEW, or ERROR verdicts
- At least two improvements
- No benign-control regression

The Day 18 candidate passes these configured rules. That means the local
showcase gate passes; it does not mean every possible AI-security risk has been
removed.

## 7. New Shared Showcase Workflow

The new package is:

```text
src/ai_red_teaming_harness/showcase/
├── __init__.py
├── models.py
└── workflow.py
```

The workflow connects existing components:

```text
Day 18 test pack
        ↓
Baseline E2E assessment
        ↓
Candidate E2E assessment
        ↓
In-memory verdict comparison
        ↓
Existing policy gate
        ↓
Safe showcase summary + manifest
```

It reuses the existing E2E, comparison, and gate rules rather than creating a
second implementation of those features.

## 8. Showcase Files

Every run creates a timestamped `SHOWCASE-*` folder. Its two top-level files
are:

```text
showcase_summary.md
showcase_manifest.json
```

The folder also contains separate sanitized E2E assessment directories for
the baseline and candidate.

`showcase_summary.md` is the human-readable demo result. It contains posture,
finding counts, test-level verdicts, outcomes, gate status, and a scope warning.

`showcase_manifest.json` is the machine-readable audit summary. It records the
workflow stages, providers, aggregate comparison counts, gate status, artifact
locations, and raw-evidence export policy.

## 9. Data-Minimization Boundary

The showcase performs comparison in memory. Its top-level summary files do not
export attack prompts or provider responses. The nested final assessments use
the existing sanitization layer.

This design reduces accidental evidence exposure during a portfolio demo. It
does not remove the need to review artifacts before sharing them.

## 10. Demo Explanation

A concise explanation is:

> I run the same five security scenarios against a deterministic vulnerable
> baseline and hardened candidate. The harness evaluates both sides, identifies
> four improvements with no regressions, verifies that normal behavior is
> preserved, and applies a strict policy gate. The exported showcase contains
> sanitized aggregate evidence and is scoped to the configured tests.

## 11. Regression Testing

Day 18 adds eight tests covering:

- Vulnerable baseline findings
- Hardened candidate behavior
- Exact comparison outcomes
- Passing policy gate
- Safe top-level artifacts
- Manifest scope and export flags
- Raw-evidence exclusion
- Rejection of identical provider roles

Expected regression result:

```text
Day 17 = 100 passed
Day 18 = 108 passed
```
