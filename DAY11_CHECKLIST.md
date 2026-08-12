# Day 11 Checklist — Repeated Runs & Stability

## Setup
- [ ] Merge Day 11 update into Day 10 project
- [ ] Replace README, pyproject and architecture
- [ ] Replace providers/factory.py
- [ ] Add mock_flaky.py
- [ ] Add stability package
- [ ] Add stability_cases.py
- [ ] Add Day 11 stability pack
- [ ] Reinstall package
- [ ] Confirm version `0.11.0`

## Validation
- [ ] Run `validate-ai-tests test_packs/day11_stability_pack.yaml`
- [ ] Confirm 3 test cases validate
- [ ] Understand that the pack contains 10 total attempts

## Hardened Stability
- [ ] Run stability command with mock-hardened
- [ ] FLK-001 = STABLE_PASS
- [ ] STB-001 = STABLE_PASS
- [ ] STB-002 = STABLE_PASS
- [ ] Summary flaky=0
- [ ] Average pass rate=100%

## Flaky Demo
- [ ] Run stability command with mock-flaky
- [ ] FLK-001 attempts=4
- [ ] FLK-001 PASS=2
- [ ] FLK-001 FAIL=2
- [ ] FLK-001 pass rate=50%
- [ ] FLK-001 status=FLAKY

## Vulnerable Demo
- [ ] Run stability command with mock-vulnerable
- [ ] FLK-001 FAIL=4
- [ ] FLK-001 pass rate=0%
- [ ] FLK-001 status=STABLE_FAIL

## Artifacts
- [ ] Confirm stability.json
- [ ] Confirm stability.csv
- [ ] Confirm stability_summary.json

## Regression
- [ ] Run `python -m pytest`
- [ ] Confirm `61 passed`
- [ ] Confirm Day 10 pack still works
- [ ] Confirm Day 8 security gate still passes

## Theory
- [ ] Explain repetition
- [ ] Explain stability
- [ ] Explain flaky
- [ ] Explain pass rate
- [ ] Explain stable fail vs flaky
- [ ] Explain why 100% observed pass rate is not a security guarantee
