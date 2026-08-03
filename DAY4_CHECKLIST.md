# Day 4 Checklist

## Files

- [ ] `reporters/` folder added
- [ ] `report_cases.py` added
- [ ] `RunSummary` model added
- [ ] `test_reporters.py` added
- [ ] README and architecture updated

## Commands

- [ ] Package installed as version `0.4.0`
- [ ] `report-ai-tests --help` works
- [ ] Vulnerable report command creates three files
- [ ] Hardened report command creates three files
- [ ] `python -m pytest` shows `19 passed`

## Understanding

- [ ] I can explain serialization
- [ ] I can explain JSON vs CSV
- [ ] I can explain flattening
- [ ] I can explain an artifact
- [ ] I can explain aggregation and run summary
- [ ] I understand why each run has a separate output directory
- [ ] I understand that reports are evidence, not proof of complete security

## GitHub Hygiene

Do not upload:

- `.venv/`
- `__pycache__/`
- `*.egg-info/`
- `.pytest_cache/`
- Real sensitive output files

Generated `output/` remains ignored. Sanitized samples can be added later under `examples/`.
