# Day 7 Checklist — Security Policy Gate and CI/CD

## Merge and Setup

- [ ] Copy the Day 7 update into the existing Day 6 project
- [ ] Replace README, pyproject and architecture files
- [ ] Add the `gates` package
- [ ] Add `gate_cases.py`
- [ ] Add `policies/strict_gate.yaml`
- [ ] Add `.github/workflows/ai-security-gate.yml`
- [ ] Add `tests/test_security_gate.py`
- [ ] Reinstall the editable package
- [ ] Confirm package version `0.7.0`

## Local Gate

- [ ] Run `gate-ai-tests`
- [ ] Confirm the forward comparison gate is `PASSED`
- [ ] Confirm each rule result is visible
- [ ] Confirm `gate_result.json` is generated
- [ ] Confirm the process exit code is 0

## Failure Demonstration

- [ ] Reverse baseline and candidate
- [ ] Confirm the gate becomes `FAILED`
- [ ] Confirm regressions are reported
- [ ] Confirm the process exit code is 1

## Automated Tests

- [ ] Run `python -m pytest`
- [ ] Confirm `37 passed`

## Theory

- [ ] Explain security gate
- [ ] Explain Policy as Code
- [ ] Explain threshold
- [ ] Explain gate status
- [ ] Explain exit codes
- [ ] Explain gate failure vs execution error
- [ ] Explain CI/CD
- [ ] Explain fail closed
- [ ] Explain benign-control regression
- [ ] Explain why passing the gate is not a full security certification

## GitHub

- [ ] Upload Day 7 source and documentation
- [ ] Confirm the Actions tab shows the workflow
- [ ] Confirm the workflow completes successfully
