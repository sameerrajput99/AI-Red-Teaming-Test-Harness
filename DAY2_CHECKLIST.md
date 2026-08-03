# Day 2 Checklist

## Files

- [ ] Replace `pyproject.toml`
- [ ] Replace `src/ai_red_teaming_harness/models.py`
- [ ] Add `src/ai_red_teaming_harness/runner.py`
- [ ] Add `src/ai_red_teaming_harness/run_cases.py`
- [ ] Add the complete `src/ai_red_teaming_harness/providers/` folder
- [ ] Add `tests/test_runner.py`
- [ ] Replace `docs/architecture.md`
- [ ] Add `docs/concepts_day2.md`
- [ ] Update `README.md`

## Commands

- [ ] Reinstall editable package: `python -m pip install -e ".[dev]"`
- [ ] Run vulnerable configuration
- [ ] Run hardened configuration
- [ ] Run `pytest`
- [ ] Confirm `8 passed`

## Understanding

- [ ] Explain provider abstraction
- [ ] Explain why mock providers are used
- [ ] Explain the runner's role
- [ ] Explain execution status versus security verdict
- [ ] Explain why raw evidence is captured before evaluation
- [ ] Explain why one provider error should not crash the complete run

## GitHub

- [ ] Upload only the Day 2 source and documentation files
- [ ] Do not upload `.venv`, `__pycache__`, `.pytest_cache` or `.egg-info`
- [ ] Use commit message: `Add provider abstraction and raw test execution engine`
