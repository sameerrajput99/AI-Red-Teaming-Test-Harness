# AI Red Teaming Test Harness v1.0.0

Version `1.0.0` completes the 20-day learning and build plan for a safe,
reproducible AI red-teaming test harness.

## Release Highlights

- Structured YAML test packs with validated schemas.
- Deterministic vulnerable, hardened, and flaky local providers.
- Optional authorized live-provider adapter.
- Configurable evaluation, comparison, stability, risk, and finding stages.
- Policy-based AI security gate for local and CI use.
- Consolidated sanitized JSON, Markdown, and static HTML assessment evidence.
- Integration and end-to-end workflow verification.
- Shared word/substring matching and fail-closed evaluator error handling.
- One-command vulnerable-versus-hardened showcase.
- Repository, security, contribution, evidence-sharing, and interview documentation.

## Verified Release Checks

```text
Regression suite              120 passed
Configured AI security gate   PASSED
Dependency compatibility      No broken requirements found
Package version               1.0.0
Python distributions          Wheel + source distribution built
```

The deterministic Day 18 showcase remains:

```text
4 improved
0 regressed
1 unchanged pass
Gate passed
```

## Important Scope Statement

These results verify the included code, mock providers, test packs, evaluators,
and configured policy. They are not a benchmark for a production model, a
penetration-test certificate, a compliance attestation, or proof of complete
AI security. Test only systems you own or are explicitly authorized to assess.

## Upgrade

From the repository root:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

Read `LIMITATIONS.md`, `SECURITY.md`, and `RELEASE_CHECKLIST.md` before sharing
results or publishing release artifacts.
