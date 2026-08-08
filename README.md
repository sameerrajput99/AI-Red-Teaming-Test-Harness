# AI Red Teaming Test Harness

A safe, local and reproducible Python framework for defining, executing, evaluating, reporting, comparing and gating structured AI security tests.

## Current Status: Day 8

The project now includes an expanded deterministic security test pack covering:

- Prompt leakage
- Prompt injection
- Instruction override
- Refusal behavior
- Hallucination indicators
- Safety boundaries
- Benign usability controls

The Day 8 pack contains **14 tests**:

```text
12 adversarial tests
2 benign controls
```

The mock vulnerable and hardened providers were expanded so the same test pack produces deterministic before-and-after evidence.

## Day 8 Expanded Pack

Validate:

```powershell
validate-ai-tests test_packs/day8_expanded_security_pack.yaml
```

Evaluate vulnerable baseline:

```powershell
evaluate-ai-tests test_packs/day8_expanded_security_pack.yaml --provider mock-vulnerable
```

Expected:

```text
PASS=2
FAIL=12
REVIEW=0
ERROR=0
```

Evaluate hardened candidate:

```powershell
evaluate-ai-tests test_packs/day8_expanded_security_pack.yaml --provider mock-hardened
```

Expected:

```text
PASS=14
FAIL=0
REVIEW=0
ERROR=0
```

Compare:

```powershell
compare-ai-tests test_packs/day8_expanded_security_pack.yaml --baseline mock-vulnerable --candidate mock-hardened
```

Expected:

```text
IMPROVED=12
REGRESSED=0
UNCHANGED_PASS=2
UNCHANGED_ISSUE=0
INDETERMINATE=0
```

Run the strict policy gate:

```powershell
gate-ai-tests test_packs/day8_expanded_security_pack.yaml --policy policies/strict_gate.yaml --baseline mock-vulnerable --candidate mock-hardened
```

Expected:

```text
Gate status: PASSED
```

## Security Coverage

| Category | Tests | Purpose |
|---|---:|---|
| Prompt leakage | 2 | Protect hidden system/developer instructions |
| Prompt injection | 2 | Resist user/document attempts to replace instruction hierarchy |
| Instruction override | 2 | Resist debug/maintenance-mode override attempts |
| Refusal behavior | 2 | Refuse requests for protected credentials/tokens |
| Hallucination | 2 | Avoid configured fabricated citation/claim markers |
| Safety boundary | 2 | Resist authorization/access-control bypass requests |
| Benign control | 2 | Preserve normal educational/helpful behavior |

## Important Day 8 Limitation

Day 8 expands **test breadth**, not evaluator sophistication.

The current deterministic evaluators still rely on:

- Forbidden patterns
- Refusal signals
- Response presence

More advanced response evaluation is intentionally reserved for a later phase. The Day 8 results therefore describe only these configured test cases and deterministic checks.

## Security Gate and CI

The GitHub Actions workflow now runs the strict gate against the expanded Day 8 pack:

```text
.github/workflows/ai-security-gate.yml
```

It requires no API key because both providers are local simulations.

## Run All Unit Tests

```powershell
python -m pytest
```

Expected after Day 8:

```text
43 passed
```

## Ethical Use

The prompts use safe local simulations and fake placeholder secrets only. This project is for defensive testing, education and authorized assessment.

Passing the expanded pack or policy gate is not a complete security certification.
