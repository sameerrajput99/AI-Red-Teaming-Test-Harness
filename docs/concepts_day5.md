# Day 5 Concepts — Baseline vs Candidate Comparison

## Objective

Day 5 adds a comparison layer. The harness now runs the same test pack against two configurations and explains how the candidate changed relative to the baseline.

## Baseline

The baseline is the reference configuration. It represents the behavior we are comparing against.

In the starter project:

```text
Baseline = mock-vulnerable
```

## Candidate

The candidate is the new or hardened configuration being assessed.

```text
Candidate = mock-hardened
```

## Why the same test pack matters

A fair comparison changes one major variable: the provider configuration. The prompts, expected behavior, severity and evaluators remain the same.

```text
Same tests + different configuration = meaningful comparison
Different tests + different configuration = unclear comparison
```

## Record alignment

Results are matched using:

```text
Test ID + Attempt Number
```

This allows repeated tests to remain traceable. Attempt 1 on the baseline is compared with attempt 1 on the candidate.

## Comparison outcomes

### IMPROVED

The candidate produced a safer verdict than the baseline.

```text
FAIL → PASS
REVIEW → PASS
FAIL → REVIEW
```

### REGRESSED

The candidate produced a worse verdict than the baseline.

```text
PASS → FAIL
PASS → REVIEW
REVIEW → FAIL
```

### UNCHANGED_PASS

Both sides passed the same test.

```text
PASS → PASS
```

This is important for benign controls because it shows that hardening did not break normal functionality.

### UNCHANGED_ISSUE

Both sides produced the same non-pass security verdict.

```text
FAIL → FAIL
REVIEW → REVIEW
```

This means the candidate did not improve that defined behavior.

### INDETERMINATE

At least one side produced an execution/evaluation error, so a reliable security comparison cannot be made.

```text
ERROR → PASS
FAIL → ERROR
```

## Regression

A regression is a security or usability behavior that became worse in the candidate.

A hardened system can reduce attack failures but accidentally block benign requests. The benign control helps detect that problem.

## Comparison summary

The summary aggregates individual comparison records:

```text
Improved = 2
Regressed = 0
Unchanged pass = 1
Unchanged issue = 0
Indeterminate = 0
```

It also includes baseline and candidate verdict counts so reviewers can see the before-and-after change.

## Comparison artifacts

### comparison.json

Preserves nested side-by-side records, raw responses, verdicts and explanations. Best for automation and later HTML/PDF generation.

### comparison.csv

Provides one row per test attempt. Best for Excel, Google Sheets, filtering and recruiter screenshots.

### comparison_summary.json

Contains compact metrics without the complete response evidence.

## Important limitation

`IMPROVED` means the candidate behaved better for the configured tests and evaluators. It does not mean the complete model or application is secure.

## Easy interview explanation

> I added a comparison engine that runs an identical test pack against a baseline and a candidate configuration. It aligns records by test ID and attempt number, compares the security verdicts, classifies improvements and regressions, and exports side-by-side evidence to JSON and CSV. The system rejects mismatched record sets rather than producing misleading comparisons.
