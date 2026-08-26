# Contributing

Contributions should preserve the harness's deterministic, defensive, and
evidence-conscious design.

## Local Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Required Verification

Run the complete regression suite:

```powershell
python -m pytest
```

Run the configured local security gate:

```powershell
gate-ai-tests test_packs/day8_expanded_security_pack.yaml `
  --policy policies/strict_gate.yaml `
  --baseline mock-vulnerable `
  --candidate mock-hardened
```

Verify dependency compatibility and build the release distributions:

```powershell
python -m pip check
python -m build
```

The current verified regression baseline is documented in `README.md`. A pull
request must not reduce coverage or silently change existing test-pack
semantics.

## Change Requirements

- Keep test-pack schemas explicit and validated.
- Add tests for every behavior change and failure boundary.
- Preserve deterministic mock-provider behavior unless the change is explained.
- Do not hard-code credentials, tokens, endpoints, or private data.
- Do not export raw prompts or responses through sanitized assessment paths.
- Escape untrusted content in HTML output.
- Update README, architecture, limitations, and day-specific concepts when the
  public behavior changes.
- Keep generated output, virtual environments, caches, and build artifacts out
  of commits.

## Pull Request Checklist

- [ ] The complete test suite passes locally.
- [ ] The strict local security gate passes.
- [ ] Dependency compatibility and package build checks pass.
- [ ] New behavior has automated tests.
- [ ] Documentation and version metadata agree.
- [ ] No secret or sensitive evidence is included.
- [ ] Limitations and scope statements remain accurate.

## Responsible Use

Only submit test scenarios designed for systems you own or are explicitly
authorized to assess. Do not include operational exploit payloads, real
credentials, customer data, or instructions for unauthorized testing.
