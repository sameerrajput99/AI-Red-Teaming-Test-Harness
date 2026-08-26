# Day 20 Checklist — Final QA & v1.0.0 Release

## Installation

- [ ] Merge the Day 20 update into the Day 19 project root.
- [ ] Activate `.venv`.
- [ ] Run `python -m pip install -e ".[dev]"`.
- [ ] Confirm package version `1.0.0`.

## Final Quality Assurance

- [ ] Run `python -m pytest`.
- [ ] Confirm `120 passed`.
- [ ] Confirm all 114 Day 1–19 tests still pass.
- [ ] Run the strict local AI security gate.
- [ ] Confirm `Gate status: PASSED`.
- [ ] Run `python -m pip check`.
- [ ] Confirm no broken requirements are reported.

## Package Build

- [ ] Remove only stale local `build/`, `dist/`, and `*.egg-info` artifacts if present.
- [ ] Run `python -m build`.
- [ ] Confirm a `1.0.0` wheel is created in `dist/`.
- [ ] Confirm a `1.0.0` source distribution is created in `dist/`.
- [ ] Do not manually upload `build/` or `dist/` to the source tree.

## Release Documentation

- [ ] Review `CHANGELOG.md`.
- [ ] Review `RELEASE_NOTES_v1.0.0.md`.
- [ ] Review `RELEASE_CHECKLIST.md`.
- [ ] Confirm README, `pyproject.toml`, package `__init__.py`, and `SECURITY.md` agree on `1.0.0`.
- [ ] Review `docs/portfolio_showcase.md` before posting publicly.

## GitHub Release

- [ ] Upload the Day 20 source update using the exact repository paths.
- [ ] Wait for the GitHub Actions security gate to pass.
- [ ] Create the tag `v1.0.0` from the verified `main` commit.
- [ ] Create a GitHub release titled `AI Red Teaming Test Harness v1.0.0`.
- [ ] Paste the reviewed release notes into the GitHub release.
- [ ] Attach build artifacts only after local verification.

## Scope Accuracy

- [ ] Describe `120 passed` as regression evidence, not security certification.
- [ ] Describe the gate as passing only for the configured policy and test pack.
- [ ] Describe mock-provider results as deterministic demonstrations, not real-model benchmarks.
- [ ] Use `NO_OBSERVED_FINDINGS within the configured scope`.
- [ ] Test only systems you own or have explicit authorization to assess.
