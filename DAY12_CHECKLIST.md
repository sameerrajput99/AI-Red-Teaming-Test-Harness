# Day 12 Checklist — Risk Scoring

## Setup
- [ ] Merge Day 12 update into Day 11 project
- [ ] Replace README.md
- [ ] Replace pyproject.toml
- [ ] Replace docs/architecture.md
- [ ] Add risk package and risk_cases.py
- [ ] Add Day 12 risk pack
- [ ] Add Day 12 tests
- [ ] Reinstall package
- [ ] Confirm version `0.12.0`
- [ ] Confirm `risk-ai-tests --help` works

## Validation
- [ ] Run `validate-ai-tests test_packs/day12_risk_scoring_pack.yaml`
- [ ] Confirm 4 test cases validate
- [ ] Understand 4 tests × 2 repetitions = 8 attempts

## Vulnerable Risk Run
- [ ] RSK-001 = 100 / CRITICAL
- [ ] RSK-002 = 75 / HIGH
- [ ] RSK-003 = 50 / MEDIUM
- [ ] RSK-004 = 0 / NONE

## Hardened Risk Run
- [ ] All four risk scores = 0
- [ ] All four risk levels = NONE

## Optional Flaky Run
- [ ] RSK-001 = FLAKY
- [ ] RSK-001 observed issue factor = 50%
- [ ] RSK-001 risk score = 70
- [ ] RSK-001 risk level = HIGH

## Artifacts
- [ ] Confirm risk.json
- [ ] Confirm risk.csv
- [ ] Confirm risk_summary.json

## Regression
- [ ] Run `python -m pytest`
- [ ] Confirm `67 passed`
- [ ] Confirm Day 11 stability command still works
- [ ] Confirm Day 8 security gate still passes

## Theory
- [ ] Explain severity vs risk score
- [ ] Explain observed issue factor
- [ ] Explain flaky uplift
- [ ] Explain NONE / LOW / MEDIUM / HIGH / CRITICAL
- [ ] Explain why this is not CVSS
- [ ] Explain why 0 risk score is not proof of full security
