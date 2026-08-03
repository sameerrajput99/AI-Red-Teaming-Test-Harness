# Day 5 Checklist — Vulnerable vs Hardened Comparison

## File setup

- [ ] Replaced `README.md`
- [ ] Replaced `pyproject.toml`
- [ ] Replaced `docs/architecture.md`
- [ ] Replaced `src/ai_red_teaming_harness/models.py`
- [ ] Added `docs/concepts_day5.md`
- [ ] Added `src/ai_red_teaming_harness/compare_cases.py`
- [ ] Added the complete `src/ai_red_teaming_harness/comparisons/` folder
- [ ] Added `tests/test_comparisons.py`

## Local verification

- [ ] Activated the current `.venv`
- [ ] Ran `python -m pip install -e ".[dev]"`
- [ ] Confirmed package version `0.5.0`
- [ ] Ran the vulnerable-vs-hardened comparison command
- [ ] Saw `PL-001` and `IO-001` classified as `IMPROVED`
- [ ] Saw `CTRL-001` classified as `UNCHANGED_PASS`
- [ ] Confirmed three comparison artifacts were generated
- [ ] Ran `python -m pytest`
- [ ] Confirmed `25 passed`

## Understanding check

- [ ] I can explain baseline and candidate configurations
- [ ] I can explain why the same test pack must be used for both sides
- [ ] I can explain improvement, regression, unchanged pass and indeterminate
- [ ] I understand that improvement does not prove complete security
- [ ] I can explain why records are aligned by test ID and attempt number
- [ ] I can explain what a comparison artifact contains

## GitHub hygiene

- [ ] Did not upload `.venv/`
- [ ] Did not upload `__pycache__/`
- [ ] Did not upload `*.egg-info/`
- [ ] Did not upload generated `output/COMPARE-*` evidence
