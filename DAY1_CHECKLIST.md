# Project 1 — Day 1 Checklist

## Build Tasks

- [ ] Open the project in VS Code
- [ ] Create and activate `.venv`
- [ ] Install the project in editable mode
- [ ] Read `docs/concepts_day1.md`
- [ ] Read `test_packs/day1_test_cases.yaml`
- [ ] Run the validation command
- [ ] Run `pytest`
- [ ] Intentionally break one YAML field and observe the error
- [ ] Restore the YAML file
- [ ] Draw the architecture in your own notebook
- [ ] Explain all three tests without reading
- [ ] Create the Git repository and first commit

## Commands

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
validate-ai-tests test_packs/day1_test_cases.yaml
pytest
```

## Understanding Check

Answer these in your own words:

1. What is a test harness?
2. What is one test case?
3. Why do we define expected behavior before execution?
4. Why is a benign control necessary?
5. What does schema validation protect us from?
6. What is the difference between severity and verdict?
7. Why do we use `safe_load()`?
8. What is a threat model?
9. What is a trust boundary?
10. What part of the complete project is not built yet?

## Day 1 Completion Evidence

Save these screenshots:

1. Folder structure in VS Code
2. Successful test-pack validation
3. `pytest` showing all tests passed
4. GitHub repository landing page after the first push
