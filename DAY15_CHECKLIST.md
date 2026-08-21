# Day 15 Checklist — Evidence Sanitization & Safe Export

## Setup
- [ ] Day 14 files are already merged locally
- [ ] Merge Day 15 update pack
- [ ] Replace README.md
- [ ] Replace pyproject.toml
- [ ] Replace docs/architecture.md
- [ ] Replace assessment/reporter.py
- [ ] Add sanitization package
- [ ] Add test_sanitization.py
- [ ] Reinstall project
- [ ] Confirm version `0.15.0`

## Concepts
- [ ] Explain sanitization
- [ ] Explain redaction
- [ ] Explain safe export
- [ ] Explain data minimization
- [ ] Explain sanitization vs HTML escaping
- [ ] Explain why regex sanitization is not perfect

## Practical
- [ ] Run `python -m pytest`
- [ ] Confirm `85 passed`
- [ ] Run vulnerable assessment
- [ ] Confirm assessment_report.json
- [ ] Confirm assessment_report.md
- [ ] Confirm assessment_report.html
- [ ] Confirm sanitization_summary.json
- [ ] Confirm raw_prompt_exported = false
- [ ] Confirm raw_response_exported = false

## Regression
- [ ] Day 14 assessment command still works
- [ ] Day 13 findings command still works
- [ ] Day 12 risk command still works
- [ ] Day 8 security gate still passes

## Sharing Safety
- [ ] Never upload `.env`
- [ ] Never intentionally put a real API key into screenshots/reports
- [ ] Review sanitized reports before external sharing
