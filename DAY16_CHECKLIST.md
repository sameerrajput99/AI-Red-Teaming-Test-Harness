# Day 16 Checklist — Integration & End-to-End Testing

## Installation

- [ ] Copy the Day 16 update into the existing Day 15 project root.
- [ ] Activate `.venv`.
- [ ] Run `python -m pip install -e ".[dev]"`.
- [ ] Confirm package version `0.16.0`.

## Regression Verification

- [ ] Run `python -m pytest`.
- [ ] Confirm `92 passed`.

## End-to-End Provider Matrix

- [ ] Run `e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-vulnerable`.
- [ ] Confirm observed posture is `CRITICAL` and three findings are created.
- [ ] Run `e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-hardened`.
- [ ] Confirm observed posture is `NO_OBSERVED_FINDINGS` and zero findings are created.
- [ ] Run `e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-flaky`.
- [ ] Confirm `RSK-001` becomes `FLAKY` and receives a non-zero risk score.

## Artifact Verification

- [ ] Confirm `assessment_report.json` exists.
- [ ] Confirm `assessment_report.md` exists.
- [ ] Confirm `assessment_report.html` exists.
- [ ] Confirm `sanitization_summary.json` exists.
- [ ] Confirm `e2e_manifest.json` exists.
- [ ] Confirm the manifest records `raw_prompt_exported=false` and `raw_response_exported=false`.

## Security Review

- [ ] No real API key is required for Day 16 tests.
- [ ] Only deterministic local providers are used.
- [ ] Raw prompts and responses are not copied into final assessment artifacts.
- [ ] Generated `output/` remains excluded from Git unless intentionally sanitized and reviewed.
