# Day 17 Concepts — Code Quality & Hardening

## 1. Day 17 Objective

Day 17 improves reliability without replacing the existing Day 1–16 pipeline.
It focuses on three quality risks:

1. Literal substring checks can create false positives.
2. An unexpected evaluator exception can interrupt an assessment.
3. Provider exception text can be excessively large or contain sensitive data.

The hardening changes preserve backward compatibility and remain deterministic.

## 2. False Positives

A false positive occurs when an automated check reports an issue that is not
actually present.

Example:

```text
Forbidden pattern: key
Response: A keyboard is an input device.
```

Simple substring matching finds `key` inside `keyboard`. If the configured rule
was intended to detect the standalone word `key`, that result is misleading.

Day 17 adds an explicit `match_scope` option:

```yaml
match_scope: substring
```

or:

```yaml
match_scope: word
```

## 3. Substring vs Word Scope

`substring` preserves the original behavior:

```text
key matches key
key matches keyboard
```

`word` requires non-word boundaries around the configured literal:

```text
key matches "the key was exposed"
key does not match "keyboard"
```

The default remains `substring`, so all existing test packs retain their prior
meaning unless they explicitly opt into word matching.

## 4. Shared Matching Helper

Before Day 17, literal matching logic existed independently in forbidden and
required-pattern evaluators.

Day 17 centralizes it in:

```text
src/ai_red_teaming_harness/evaluators/matching.py
```

Both evaluators now share:

- Pattern normalization
- Case-sensitive or case-insensitive comparison
- Substring matching
- Word-scoped matching

This reduces duplicated logic and makes future changes easier to test.

## 5. Case Sensitivity

Case-insensitive matching treats `SECRET`, `Secret`, and `secret` as equivalent.

Case-sensitive matching treats them as different strings.

Day 17 ensures literal forbidden-pattern evaluation follows the configured
`case_sensitive` value. Existing configurations remain case-insensitive by
default.

## 6. Fail-Closed Evaluator Boundary

An evaluator is application code and may fail because of a bug or unexpected
input. Silently treating that situation as a pass would be unsafe.

Day 17 converts unexpected evaluator exceptions into:

```text
security_verdict = ERROR
```

The complete process remains alive, but the affected record cannot be mistaken
for a successful security result.

This is fail-closed behavior:

```text
Evaluator exception
        ↓
Structured ERROR finding
        ↓
Composite verdict ERROR
```

The original exception detail is not copied into the finding because it may
contain secrets or internal implementation information.

## 7. Provider Error Hardening

Provider failures were already converted into execution evidence. Day 17 adds
two protections to the stored error detail:

1. Supported secret patterns are redacted with the existing Day 15 sanitizer.
2. The diagnostic detail is limited to 500 characters.

Example:

```text
RuntimeError: API_KEY=ULTRASECRET999
```

Stored result:

```text
RuntimeError: API_KEY=[REDACTED_SECRET]
```

This is defense in depth. Redaction is pattern-based and cannot guarantee that
every possible sensitive value will be recognized.

## 8. Unit and Regression Testing

Day 17 adds eight tests covering:

- Substring false-positive prevention
- Standalone word detection
- Case-sensitive forbidden patterns
- Partial required-pattern rejection
- Evaluator exception containment
- Provider error secret redaction
- Provider error length bounding
- Vulnerable/hardened Day 17 provider matrix

Regression result:

```text
Day 16 = 92 passed
Day 17 = 100 passed
```

Passing tests demonstrate the configured code paths and contracts. They do not
prove that every real provider or every semantic security issue is covered.
