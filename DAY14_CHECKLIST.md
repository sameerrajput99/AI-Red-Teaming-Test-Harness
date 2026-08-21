# Day 14 Checklist — Final Reporting Layer

## Setup
- [ ] Day 13 completed successfully
- [ ] Merge Day 14 update pack
- [ ] Replace README.md
- [ ] Replace pyproject.toml
- [ ] Replace docs/architecture.md
- [ ] Add assessment package
- [ ] Add assessment_cases.py
- [ ] Add test_assessment_reporting.py
- [ ] Reinstall project
- [ ] Confirm version `0.14.0`
- [ ] Confirm `assessment-ai-tests --help` works

## Concepts
- [ ] Explain why a final reporting layer is needed
- [ ] Explain observed assessment posture
- [ ] Explain NO_OBSERVED_FINDINGS correctly
- [ ] Explain Executive Summary
- [ ] Explain Prioritized Actions
- [ ] Explain JSON vs Markdown vs HTML output
- [ ] Explain why HTML escaping matters
- [ ] Explain report != full security certification

## Vulnerable Demo
- [ ] Run assessment with mock-vulnerable
- [ ] Confirm posture = CRITICAL
- [ ] Confirm tests assessed = 4
- [ ] Confirm findings = 3
- [ ] Confirm critical = 1
- [ ] Confirm high = 1
- [ ] Confirm highest risk = 100

## Hardened Demo
- [ ] Run assessment with mock-hardened
- [ ] Confirm posture = NO_OBSERVED_FINDINGS
- [ ] Confirm findings = 0
- [ ] Confirm highest risk = 0

## Artifacts
- [ ] Confirm assessment_report.json
- [ ] Confirm assessment_report.md
- [ ] Confirm assessment_report.html
- [ ] Open the HTML report in a browser

## Regression
- [ ] Run `python -m pytest`
- [ ] Confirm `79 passed`
- [ ] Confirm Day 13 findings command still works
- [ ] Confirm Day 12 risk command still works
- [ ] Confirm Day 8 security gate still passes
