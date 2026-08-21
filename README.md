# AI Red Teaming Test Harness

A safe, reproducible Python framework for structured AI red teaming,
deterministic evaluation, stability analysis, risk prioritization, normalized
findings, sanitized assessment reporting, and end-to-end verification.

## Current Status

| Item | Value |
| --- | --- |
| Project phase | Day 16 complete |
| Package version | `0.16.0` |
| Python | `3.10+` |
| Regression baseline | `92 passed` |
| License | MIT |

## What the Harness Does

The project turns adversarial prompts into repeatable, reviewable security
tests. It can:

- Validate structured YAML test packs before execution.
- Run deterministic vulnerable, hardened, and flaky mock providers.
- Optionally run an authorized OpenAI-backed provider.
- Evaluate responses with configurable deterministic checks.
- Export structured JSON, CSV, Markdown, and safe static HTML evidence.
- Compare baseline and candidate provider behaviour.
- Enforce a policy-based AI security gate in CI.
- Analyze repeated-run stability.
- Calculate project-specific risk scores.
- Convert non-zero risks into normalized security findings.
- Build consolidated assessment reports.
- Redact configured sensitive-data patterns before final export.
- Verify the complete pipeline with integration and E2E tests.

## Architecture

```text
YAML Test Pack
      ↓
Validation
      ↓
Provider Execution
      ↓
Deterministic Evaluation
      ↓
Stability Analysis
      ↓
Risk Scoring
      ↓
Normalized Findings
      ↓
Assessment Building
      ↓
Sanitization
      ↓
Safe Assessment Artifacts
      ↓
E2E Manifest
```

Day 16 orchestrates the existing production components; it does not duplicate
their evaluator, scoring, findings, assessment, or sanitization logic.

## Providers

| Provider | Purpose |
| --- | --- |
| `mock-vulnerable` | Deterministic unsafe baseline for defensive tests |
| `mock-hardened` | Deterministic safer candidate for regression comparison |
| `mock-flaky` | Alternates configured behaviour to exercise stability logic |
| `openai-live` | Optional authorized live-model adapter using environment configuration |

The automated regression and Day 16 E2E tests use local mock providers and do
not require a real API key.

## Quick Start

### 1. Clone the repository

```powershell
git clone https://github.com/sameerrajput99/AI-Red-Teaming-Test-Harness.git
cd AI-Red-Teaming-Test-Harness
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### 3. Install the project and development dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 4. Run the regression suite

```powershell
python -m pytest
```

Expected baseline:

```text
92 passed
```

## Day 16 End-to-End Verification

Run the complete local assessment pipeline with one provider:

```powershell
e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-vulnerable
```

Other deterministic profiles:

```powershell
e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-hardened
e2e-ai-tests test_packs/day12_risk_scoring_pack.yaml --provider mock-flaky
```

Verified local profiles for the included Day 12 pack:

| Provider | Executions | Findings | Observed posture |
| --- | ---: | ---: | --- |
| `mock-vulnerable` | 8 | 3 | `CRITICAL` |
| `mock-hardened` | 8 | 0 | `NO_OBSERVED_FINDINGS` |
| `mock-flaky` | 8 | 1 | `HIGH` |

These results describe the included deterministic test configuration. They are
not a general security rating for real language models.

## Day 16 Safe Artifacts

Each successful E2E run creates a timestamped folder under `output/` containing:

```text
assessment_report.json
assessment_report.md
assessment_report.html
sanitization_summary.json
e2e_manifest.json
```

The manifest records stage counts, observed posture, the expected artifact set,
and the configured raw-evidence export policy.

## Command Reference

```text
validate-ai-tests   Validate a YAML test pack
run-ai-tests        Execute tests against a provider
evaluate-ai-tests   Evaluate provider responses
report-ai-tests     Export structured execution evidence
compare-ai-tests    Compare baseline and candidate providers
gate-ai-tests       Enforce a configured security policy
check-ai-provider   Validate provider configuration
stability-ai-tests  Analyze repeated-run behaviour
risk-ai-tests       Calculate risk records
findings-ai-tests   Build normalized security findings
assessment-ai-tests Build sanitized assessment reports
e2e-ai-tests        Run the complete Day 16 workflow
```

Use `--help` with any command for its current arguments. Example:

```powershell
e2e-ai-tests --help
```

## Optional Live Provider

Copy the example configuration locally:

```powershell
Copy-Item .env.example .env
```

Then set values available to your own authorized account:

```text
OPENAI_API_KEY
OPENAI_MODEL
OPENAI_BASE_URL
OPENAI_TIMEOUT_SECONDS
OPENAI_MAX_RETRIES
```

Never commit `.env` or place a real key in `.env.example`, documentation,
screenshots, test packs, or generated reports.

## Security and Evidence Handling

- Test only systems you own or are explicitly authorized to assess.
- Use fictional or approved data in adversarial test packs.
- Keep `.env`, virtual environments, caches, build artifacts, and generated
  `output/` evidence out of Git.
- Treat regex-based sanitization as defense in depth, not perfect secret
  detection.
- Review sanitized artifacts before sharing them externally.
- Interpret `NO_OBSERVED_FINDINGS` only within the configured assessment scope.

The static HTML assessment renderer escapes untrusted report text and includes a
restrictive Content Security Policy.

## CI Security Gate

The GitHub Actions workflow runs:

```text
python -m pytest
```

and then evaluates the expanded security pack using the strict local gate:

```powershell
gate-ai-tests test_packs/day8_expanded_security_pack.yaml `
  --policy policies/strict_gate.yaml `
  --baseline mock-vulnerable `
  --candidate mock-hardened
```

A passing gate applies only to the configured policy, test pack, providers, and
evaluators.

## Project Structure

```text
AI-Red-Teaming-Test-Harness/
├── .github/workflows/       # Regression tests and security gate
├── docs/                    # Architecture and Day 1–16 concepts
├── policies/                # Security-gate policy
├── src/ai_red_teaming_harness/
│   ├── assessment/          # Consolidated assessment model and export
│   ├── comparisons/         # Baseline-vs-candidate comparison
│   ├── e2e/                 # Day 16 orchestration and manifest
│   ├── evaluators/          # Deterministic response checks
│   ├── findings/            # Normalized finding generation
│   ├── gates/               # Policy enforcement
│   ├── providers/           # Mock and optional live providers
│   ├── risk/                # Risk scoring
│   ├── sanitization/        # Safe-export redaction
│   └── stability/           # Repeated-run analysis
├── test_packs/              # Structured YAML security scenarios
├── tests/                   # Automated regression tests
├── LIMITATIONS.md
├── LICENSE
└── pyproject.toml
```

## Limitations

Read [LIMITATIONS.md](LIMITATIONS.md) before interpreting or sharing assessment
results. A passing test, gate, or E2E run is evidence within a configured scope;
it is not complete security certification.

## License

This repository is licensed under the [MIT License](LICENSE).
