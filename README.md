# AI Red Teaming Test Harness

A safe, reproducible Python framework for defining, executing, evaluating, reporting, comparing, gating and stability-testing structured AI security tests.

## Current Status: Day 11

Day 11 makes the existing `repetitions` field useful at analysis time.

A test can now be run multiple times and summarized as:

```text
STABLE_PASS
STABLE_FAIL
STABLE_REVIEW
STABLE_ERROR
FLAKY
```

## Why Repeat the Same Test?

A single PASS can be misleading when an AI system behaves differently across runs.

Example:

```text
Attempt 1 -> PASS
Attempt 2 -> FAIL
Attempt 3 -> PASS
Attempt 4 -> FAIL
```

A single final verdict hides the instability.

Day 11 instead reports:

```text
PASS=2
FAIL=2
Pass Rate=50%
Status=FLAKY
```

## Day 11 Demo Pack

The pack contains three tests and ten total attempts:

```text
FLK-001  repetitions=4
STB-001  repetitions=3
STB-002  repetitions=3
```

Validate:

```powershell
validate-ai-tests test_packs/day11_stability_pack.yaml
```

## Hardened Stability Run

```powershell
stability-ai-tests test_packs/day11_stability_pack.yaml --provider mock-hardened
```

Expected:

```text
FLK-001  4 attempts  4 PASS  0 FAIL  100%  STABLE_PASS
STB-001  3 attempts  3 PASS  0 FAIL  100%  STABLE_PASS
STB-002  3 attempts  3 PASS  0 FAIL  100%  STABLE_PASS

Summary:
tests=3
attempts=10
stable_pass=3
stable_issue=0
flaky=0
avg_pass_rate=100%
```

## Flaky Demonstration

```powershell
stability-ai-tests test_packs/day11_stability_pack.yaml --provider mock-flaky
```

Expected key result:

```text
FLK-001
Attempts=4
PASS=2
FAIL=2
Pass Rate=50%
Status=FLAKY
```

The local `mock-flaky` provider deliberately alternates safe and unsafe behavior only for the repeated system-prompt test. This is a deterministic demonstration of inconsistent behavior.

## Vulnerable Stability Run

```powershell
stability-ai-tests test_packs/day11_stability_pack.yaml --provider mock-vulnerable
```

Expected key result:

```text
FLK-001
Attempts=4
PASS=0
FAIL=4
Pass Rate=0%
Status=STABLE_FAIL
```

A stable failure is not flaky. It is consistently failing.

## Stability Artifacts

Each stability run creates:

```text
output/
└── STABILITY-<timestamp>-<id>/
    ├── stability.json
    ├── stability.csv
    └── stability_summary.json
```

## Important Meanings

### Pass Rate

```text
PASS attempts / total attempts × 100
```

Example:

```text
2 PASS out of 4 attempts = 50% pass rate
```

### Flaky

A test is flaky when repeated attempts do not all produce the same verdict.

### Stable Issue

A test can be perfectly stable but still bad:

```text
FAIL, FAIL, FAIL, FAIL
```

That is `STABLE_FAIL`, not `FLAKY`.

## Regression Tests

```powershell
python -m pytest
```

Expected after Day 11:

```text
61 passed
```

## Important Limitation

Repeated testing measures observed consistency only.

A 100% pass rate across a small number of attempts does not prove future behavior will always pass or that the system is fully secure.
