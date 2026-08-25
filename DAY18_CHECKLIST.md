# Day 18 Checklist — Demo & Showcase Scenario

## Installation

- [ ] Merge the Day 18 update into the Day 17 project root.
- [ ] Activate `.venv`.
- [ ] Run `python -m pip install -e ".[dev]"`.
- [ ] Confirm package version `0.18.0`.

## Regression Verification

- [ ] Run `python -m pytest`.
- [ ] Confirm `108 passed`.
- [ ] Confirm all 100 Day 1–17 tests still pass.

## Showcase Pack

- [ ] Validate `test_packs/day18_showcase_pack.yaml`.
- [ ] Explain the four adversarial cases and one benign control.
- [ ] Confirm the vulnerable baseline records four FAIL verdicts.
- [ ] Confirm the hardened candidate records five PASS verdicts.
- [ ] Confirm the benign control remains a PASS on both sides.

## Showcase Command

- [ ] Run `showcase-ai-security` from the project root.
- [ ] Confirm four `IMPROVED` outcomes.
- [ ] Confirm zero regressions.
- [ ] Confirm the strict policy gate reports `PASSED`.
- [ ] Locate `showcase_summary.md`.
- [ ] Locate `showcase_manifest.json`.

## Safe Sharing

- [ ] Confirm the showcase manifest reports raw prompt export as false.
- [ ] Confirm the showcase manifest reports raw response export as false.
- [ ] Share only reviewed sanitized artifacts.
- [ ] State that deterministic mock results are not production certification.
- [ ] Keep the complete generated `output/` directory out of Git.

## Demo Practice

- [ ] Explain baseline, candidate, outcome, and gate in simple words.
- [ ] Deliver the 30-second recruiter explanation.
- [ ] Deliver the two-minute technical walkthrough.
- [ ] Explain why the benign control prevents security-only tunnel vision.
- [ ] Answer why the same test pack must be used for both providers.
