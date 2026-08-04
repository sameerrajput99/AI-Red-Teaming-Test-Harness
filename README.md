# AI Red Teaming Test Harness

A safe, local and reproducible Python framework for defining, executing, evaluating, reporting and comparing structured AI security tests.

## Current Status: Working Local MVP

The project can now:

- Validate structured YAML test packs
- Execute the same tests against mock vulnerable and hardened configurations
- Capture raw prompts, responses, errors, latency and timestamps
- Evaluate responses as `PASS`, `FAIL`, `REVIEW` or `ERROR`
- Export full evidence to JSON, flat CSV and compact summary JSON
- Compare a baseline configuration with a candidate configuration test by test
- Classify each change as `IMPROVED`, `REGRESSED`, `UNCHANGED_PASS`, `UNCHANGED_ISSUE` or `INDETERMINATE`
- Export side-by-side comparison evidence to JSON and CSV

## Current Limitations

The current implementation uses deterministic local mock providers and a small starter test pack.

Its evaluators rely on configured response checks and may produce false positives, false negatives or ambiguous results.

A passing result applies only to the configured test case and evaluator rules. It does not prove that an AI system is fully secure.

See [LIMITATIONS.md](LIMITATIONS.md) for complete scope and interpretation guidance.

## Architecture

```text
YAML Test Pack
      ↓
Safe YAML Loader
      ↓
Schema Validation
      ↓
Validated TestCase Objects
      ↓
Test Runner
      ↓
Provider Abstraction
      ├── Baseline Configuration
      └── Candidate Configuration
      ↓
Raw Execution Records
      ↓
Security Evaluators
      ↓
Evaluated Records
      ├── Run Reports
      └── Comparison Engine
              ↓
       Side-by-Side Outcomes
              ↓
       Comparison Artifacts
       ├── comparison.json
       ├── comparison.csv
       └── comparison_summary.json
```

## Setup on Windows PowerShell

```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Validate a Test Pack

```powershell
validate-ai-tests test_packs/day1_test_cases.yaml
```

## Run Raw Execution Only

```powershell
run-ai-tests test_packs/day1_test_cases.yaml --provider mock-vulnerable
```

## Run Security Evaluation

```powershell
evaluate-ai-tests test_packs/day1_test_cases.yaml --provider mock-hardened
```

## Generate One-Provider Evidence Reports

```powershell
report-ai-tests test_packs/day1_test_cases.yaml --provider mock-vulnerable
```

## Compare Baseline and Candidate Configurations

```powershell
compare-ai-tests test_packs/day1_test_cases.yaml \
  --baseline mock-vulnerable \
  --candidate mock-hardened
```

PowerShell also accepts the command on one line:

```powershell
compare-ai-tests test_packs/day1_test_cases.yaml --baseline mock-vulnerable --candidate mock-hardened
```

Expected comparison:

```text
PL-001    FAIL → PASS    IMPROVED
IO-001    FAIL → PASS    IMPROVED
CTRL-001  PASS → PASS    UNCHANGED_PASS
```

Generated structure:

```text
output/
└── COMPARE-<timestamp>-<id>/
    ├── comparison.json
    ├── comparison.csv
    └── comparison_summary.json
```

## Comparison Meaning

- `IMPROVED`: candidate verdict is safer than baseline for the same test
- `REGRESSED`: candidate verdict is worse than baseline
- `UNCHANGED_PASS`: both configurations passed
- `UNCHANGED_ISSUE`: both configurations produced the same non-pass verdict
- `INDETERMINATE`: an execution/evaluation error prevents a reliable comparison

The comparison describes only the configured test pack and evaluators. It does not prove that the candidate configuration is fully secure.

## Run Unit Tests

```powershell
python -m pytest
```

Expected current test result:

```text
25 passed

```
## Current Development Focus

The next development phase includes:

- Expanding the structured test library
- Adding prompt-injection and refusal-behaviour scenarios
- Analysing false positives and ambiguous responses
- Publishing sanitised example evidence
- Improving repeated-run evaluation
- Preparing a short terminal demonstration

## Ethical Use

This project is intended for safe local simulation, defensive testing, education and authorized security assessment only.
