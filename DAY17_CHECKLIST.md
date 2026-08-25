# Day 17 Checklist — Code Quality & Hardening

## Installation

- [ ] Merge the Day 17 update into the Day 16 project root.
- [ ] Activate `.venv`.
- [ ] Run `python -m pip install -e ".[dev]"`.
- [ ] Confirm package version `0.17.0`.

## Regression Verification

- [ ] Run `python -m pytest`.
- [ ] Confirm `100 passed`.
- [ ] Confirm all 92 Day 1–16 tests still pass.

## False-Positive Controls

- [ ] Explain substring matching.
- [ ] Explain whole-word matching.
- [ ] Explain why `key` should not match `keyboard` in word mode.
- [ ] Explain why `authentication` should not match `reauthentication` in word mode.
- [ ] Confirm legacy test packs keep `match_scope=substring` by default.
- [ ] Confirm `case_sensitive` is enforced by literal forbidden-pattern checks.

## Error Hardening

- [ ] Confirm an evaluator exception becomes a structured `ERROR` finding.
- [ ] Confirm one evaluator failure does not crash the Python process.
- [ ] Confirm evaluator exception details are not copied into findings.
- [ ] Confirm provider error details are bounded to 500 characters.
- [ ] Confirm supported secrets in provider error messages are redacted.

## Day 17 Pack

- [ ] Run `validate-ai-tests test_packs/day17_hardening_pack.yaml`.
- [ ] Confirm three test cases validate.
- [ ] Evaluate the pack with `mock-vulnerable`.
- [ ] Confirm `PASS=2`, `FAIL=1`, `REVIEW=0`, `ERROR=0`.
- [ ] Evaluate the pack with `mock-hardened`.
- [ ] Confirm `PASS=3`, `FAIL=0`, `REVIEW=0`, `ERROR=0`.

## Existing Security Gate

- [ ] Run the strict Day 8 security gate.
- [ ] Confirm `Gate status: PASSED`.

## Sharing Safety

- [ ] Do not upload `.venv`, caches, build output, or generated evidence.
- [ ] Never use a real secret to test redaction.
- [ ] Treat deterministic matching as scoped evidence, not full semantic analysis.
