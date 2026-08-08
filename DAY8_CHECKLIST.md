# Day 8 Checklist — Expanded Security Test Coverage

## Merge and Setup

- [ ] Copy the Day 8 update into the existing Day 7 project
- [ ] Replace README, pyproject and architecture files
- [ ] Replace both mock provider files
- [ ] Add `day8_expanded_security_pack.yaml`
- [ ] Add `test_expanded_security_pack.py`
- [ ] Replace the GitHub Actions workflow
- [ ] Add `concepts_day8.md`
- [ ] Reinstall package version `0.8.0`

## Validation

- [ ] Run `validate-ai-tests test_packs/day8_expanded_security_pack.yaml`
- [ ] Confirm 14 test cases validate successfully
- [ ] Confirm all seven categories are represented

## Vulnerable Baseline

- [ ] Evaluate `mock-vulnerable`
- [ ] Confirm PASS=2
- [ ] Confirm FAIL=12
- [ ] Confirm REVIEW=0
- [ ] Confirm ERROR=0

## Hardened Candidate

- [ ] Evaluate `mock-hardened`
- [ ] Confirm PASS=14
- [ ] Confirm FAIL=0
- [ ] Confirm REVIEW=0
- [ ] Confirm ERROR=0

## Comparison and Gate

- [ ] Compare vulnerable vs hardened
- [ ] Confirm IMPROVED=12
- [ ] Confirm UNCHANGED_PASS=2
- [ ] Confirm REGRESSED=0
- [ ] Run strict security gate
- [ ] Confirm Gate status = PASSED
- [ ] Confirm exit code = 0

## Automated Tests

- [ ] Run `python -m pytest`
- [ ] Confirm `43 passed`

## Theory

- [ ] Explain test coverage
- [ ] Explain threat coverage
- [ ] Explain taxonomy
- [ ] Explain test diversity
- [ ] Explain benign controls
- [ ] Explain regression fixture
- [ ] Explain deterministic simulation
- [ ] Explain coverage vs assurance
- [ ] Explain the Day 8 hallucination-test limitation

## GitHub

- [ ] Upload Day 8 source, test pack, docs and workflow changes
- [ ] Confirm GitHub Actions uses the expanded Day 8 pack
- [ ] Confirm the workflow is green
