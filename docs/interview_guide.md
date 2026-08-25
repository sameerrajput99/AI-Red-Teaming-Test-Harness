# Interview Guide

## Project Introduction

> The AI Red Teaming Test Harness is a Python project for defining adversarial
> AI tests in YAML, executing them through provider adapters, evaluating the
> responses deterministically, comparing vulnerable and hardened behavior, and
> producing reviewable security evidence.

## Common Questions

### What problem does the project solve?

Manual prompts are difficult to repeat and compare consistently. The harness
turns security scenarios into versioned test cases with explicit expectations,
automated verdicts, evidence, and policy gates.

### Why use YAML test packs?

YAML separates security scenarios from Python implementation. Test authors can
review IDs, categories, prompts, severity, repetition counts, and evaluator
configuration without modifying the runner.

### Why are mock providers included?

They produce predictable local responses, so regression tests and demos remain
repeatable, offline, and free from live-model cost or behavior changes. They are
simulations, not benchmarks for real providers.

### What is the difference between integration and E2E testing here?

Integration tests verify connected component contracts. E2E tests exercise the
complete path from YAML loading to sanitized assessment artifacts. The project
uses both because they answer different questions.

### How does evaluation work?

Each test configures deterministic evaluators such as forbidden patterns,
required patterns, refusal signals, regex rules, response presence, or response
length. Their findings are combined conservatively into `PASS`, `FAIL`,
`REVIEW`, or `ERROR`.

### What was improved in Day 17?

Forbidden and required-pattern evaluators now share one literal-matching helper.
It supports explicit substring or whole-word scope and case handling. Evaluator
exceptions fail closed as structured `ERROR` results, while provider exception
details are redacted and bounded.

### What does the Day 18 showcase prove?

It proves that the included deterministic test pack, providers, evaluators,
comparison rules, and policy gate work together as configured. It does not
prove general security for a production model.

### Why include a benign control?

Security hardening should stop unsafe behavior without unnecessarily blocking
ordinary allowed requests. A benign control helps detect that regression.

### What is the policy gate?

It converts comparison evidence into a release-style decision using explicit
thresholds such as maximum regressions, maximum candidate failures, minimum
improvements, and benign-control preservation.

### How is evidence protected?

Final assessment exports use a sanitization layer, normalized findings avoid
copying full responses, HTML output escapes untrusted text, secrets remain in
environment variables, and top-level showcase files exclude raw prompts and
responses.

### Why is `NO_OBSERVED_FINDINGS` used instead of `secure`?

Automated tests cover only configured scenarios and evaluator rules. The phrase
accurately describes the evidence without claiming that every vulnerability has
been excluded.

## Architecture Answer

```text
YAML tests → provider → evaluation → stability → risk → findings
→ assessment → sanitization → E2E evidence → comparison → policy gate
```

Every stage has a focused responsibility, and later workflows reuse earlier
components rather than duplicating their security logic.

## Honest Limitations to Mention

- Deterministic pattern matching does not fully understand semantic meaning.
- Mock providers do not reproduce production-model variability.
- Included attack coverage is not exhaustive.
- Regex sanitization cannot guarantee detection of every sensitive value.
- Risk scores are project-specific and are not CVSS.
- Human review remains necessary for ambiguous and externally shared evidence.
