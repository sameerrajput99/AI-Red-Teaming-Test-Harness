# Architecture Through Day 11

```text
Test Pack
   ↓
TestCase.repetitions
   ↓
Runner
   ↓
Repeated Execution Records
   ↓
Evaluators
   ↓
Repeated Evaluated Records
   ↓
Stability Analyzer
   ├── PASS count
   ├── FAIL count
   ├── REVIEW count
   ├── ERROR count
   ├── Pass rate
   └── Stability status
          ↓
   STABLE_PASS
   STABLE_FAIL
   STABLE_REVIEW
   STABLE_ERROR
   FLAKY
          ↓
Stability Reports
   ├── stability.json
   ├── stability.csv
   └── stability_summary.json
```

## Existing Repetition Support

The runner already executes each test according to its `repetitions` value.

Day 11 does not invent repeated execution from scratch. It adds an analysis layer that makes those repetitions meaningful.

## Stability Rule

```text
One unique verdict across all attempts
→ stable

More than one unique verdict
→ flaky
```

Examples:

```text
PASS PASS PASS PASS
→ STABLE_PASS

FAIL FAIL FAIL FAIL
→ STABLE_FAIL

PASS FAIL PASS FAIL
→ FLAKY
```

## Pass Rate

```text
pass_rate = PASS attempts / total attempts × 100
```

Pass rate and stability are related but different.

```text
100% + stable
→ STABLE_PASS

0% + stable
→ STABLE_FAIL

50% + mixed verdicts
→ FLAKY
```

## Why Mock Flaky Exists

`mock-flaky` is a local teaching provider.

It alternates one repeated attack between:

```text
unsafe leak
safe refusal
unsafe leak
safe refusal
```

This makes flakiness reproducible for unit tests and demos.

It is not presented as a real production model.

## Important Limitation

Stability metrics describe only the observed repeated attempts.

They are not a probability guarantee about all future model behavior.
