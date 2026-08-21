# Day 13 Checklist — Security Findings Model

## Setup
- [ ] Day 12 project is already merged
- [ ] Merge Day 13 update pack
- [ ] Replace README.md
- [ ] Replace pyproject.toml
- [ ] Replace docs/architecture.md
- [ ] Add findings package
- [ ] Add findings_cases.py
- [ ] Add test_findings.py
- [ ] Reinstall project
- [ ] Confirm version `0.13.0`
- [ ] Confirm `findings-ai-tests --help` works

## Concepts
- [ ] Explain Test Case vs Security Finding
- [ ] Explain why zero-risk tests do not become findings
- [ ] Explain Finding ID
- [ ] Explain Observation
- [ ] Explain Impact
- [ ] Explain Recommendation
- [ ] Explain Evidence Summary
- [ ] Understand `OPEN` is an initial finding lifecycle state

## Vulnerable Demo
- [ ] Run Day 12 pack with `findings-ai-tests`
- [ ] Confirm FND-RSK-001 = CRITICAL / 100
- [ ] Confirm FND-RSK-002 = HIGH / 75
- [ ] Confirm FND-RSK-003 = MEDIUM / 50
- [ ] Confirm RSK-004 creates no finding
- [ ] Confirm total findings = 3

## Hardened Demo
- [ ] Run Day 12 pack with mock-hardened
- [ ] Confirm total findings = 0
- [ ] Understand zero findings is not full security certification

## Artifacts
- [ ] Confirm findings.json
- [ ] Confirm findings.csv
- [ ] Confirm findings_summary.json

## Regression
- [ ] Run `python -m pytest`
- [ ] Confirm `73 passed`
- [ ] Confirm Day 12 risk command still works
- [ ] Confirm Day 8 security gate still passes
