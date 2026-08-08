# Day 6 Checklist — Secure HTML Reporting

## Implementation

- [ ] Replace the Day 6 update files in the existing project
- [ ] Add `reporters/html_reporter.py`
- [ ] Add `comparisons/html_reporter.py`
- [ ] Add `tests/test_html_reports.py`
- [ ] Confirm package version is `0.6.0`
- [ ] Reinstall the editable package

## Run Reports

- [ ] Run a vulnerable provider report
- [ ] Confirm `results.html` is generated
- [ ] Open `results.html` in a browser
- [ ] Confirm the summary shows 1 PASS and 2 FAIL
- [ ] Confirm test IDs, prompts, responses and findings are visible

## Comparison Reports

- [ ] Run the baseline-versus-candidate comparison
- [ ] Confirm `comparison.html` is generated
- [ ] Open `comparison.html` in a browser
- [ ] Confirm PL-001 and IO-001 are IMPROVED
- [ ] Confirm CTRL-001 is UNCHANGED_PASS

## Security Understanding

- [ ] Explain presentation layer
- [ ] Explain static and self-contained HTML
- [ ] Explain HTML escaping
- [ ] Explain input validation vs output encoding
- [ ] Explain XSS risk
- [ ] Explain Content Security Policy
- [ ] Explain why HTML does not replace JSON and CSV
- [ ] Explain why a polished report is not a security certification

## Regression Test

- [ ] Run `python -m pytest`
- [ ] Confirm `31 passed`
