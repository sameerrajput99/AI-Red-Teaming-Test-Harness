# Architecture Through Day 20

```text
Structured Test Pack
        ↓
Provider Execution
        ↓
Deterministic Evaluators
        ├── Shared literal matcher
        ├── Substring or word scope
        ├── Case-sensitivity control
        └── Fail-closed exception boundary
        ↓
Stability Analysis
        ↓
Risk Scoring
        ↓
Normalized Findings
        ↓
Assessment Builder
        ↓
Assessment Report (in memory)
        ↓
Sanitization Layer
        ├── API-key redaction
        ├── bearer-token redaction
        ├── generic secret redaction
        └── email redaction
        ↓
Sanitized Assessment Copy
        ↓
Safe Export
        ├── assessment_report.json
        ├── assessment_report.md
        ├── assessment_report.html
        └── sanitization_summary.json
        ↓
End-to-End Verification Manifest
        └── e2e_manifest.json
        ↓
Day 18 Showcase Orchestrator
        ├── Vulnerable baseline E2E
        ├── Hardened candidate E2E
        ├── In-memory verdict comparison
        ├── Existing strict policy gate
        └── Safe aggregate export
                ├── showcase_summary.md
                └── showcase_manifest.json
        ↓
Day 19 Repository Trust Layer
        ├── README navigation
        ├── Demo walkthrough
        ├── Interview guide
        ├── Evidence-sharing guide
        ├── Security policy
        ├── Contribution contract
        └── Repository-quality tests
        ↓
Day 20 Release Trust Layer
        ├── Version 1.0.0 consistency
        ├── Complete regression verification
        ├── Configured security gate
        ├── Dependency compatibility check
        ├── Wheel and source distribution build
        ├── Release notes and changelog
        └── Release-readiness tests
```

## Day 20 Release Boundary

Day 20 packages the verified Day 1–19 implementation as version `1.0.0`. It
does not change provider behavior, evaluator semantics, risk scoring, findings,
sanitization, comparison, gate, or showcase algorithms.

The release layer verifies version consistency, the complete regression suite,
the configured local security gate, installed dependency compatibility, and
the ability to build standard Python wheel and source distributions. Release
notes and portfolio material describe only the verified local scope.

A successful build proves that the repository can produce installable package
artifacts. It is not a code-signing guarantee, supply-chain audit, penetration
test, or production security certification.

## Day 19 Repository Boundary

Day 19 does not alter the provider, evaluator, risk, finding, assessment,
sanitization, comparison, gate, or showcase algorithms. It adds a repository
trust layer around the verified runtime.

The README is the entry point. It links to focused documents for architecture,
demonstration, interview explanation, limitations, evidence sharing, security
reporting, and contribution requirements.

Repository-quality tests verify version consistency, required documentation,
relative README links, secret/evidence guidance, ignore rules, and the exact
scoped values shown in the showcase visual.

## Day 18 Showcase Boundary

The `showcase` workflow runs the same validated pack through two complete E2E
assessments. It compares their typed evaluation records in memory, applies the
existing gate engine, and writes a small aggregate demo layer.

The top-level showcase files contain identifiers, verdicts, counts, postures,
outcomes, gate status, and artifact locations. They do not contain the raw test
prompts or provider responses. Baseline and candidate final assessments retain
the Day 15 sanitized-export boundary.

The showcase orchestrator does not reimplement provider execution, evaluation,
stability, risk, finding, assessment, sanitization, comparison, or gate rules.

## Day 17 Hardening Boundary

The shared literal matcher centralizes normalization, case handling, substring
matching, and whole-word matching for forbidden and required-pattern
evaluators. Existing configurations continue to use substring matching unless
`match_scope: word` is explicitly configured.

Unexpected evaluator exceptions are converted into structured `ERROR`
findings. They do not become passes and do not terminate the complete process.

Provider exception details are passed through the existing sanitization rules
and limited to 500 characters before they are stored in execution evidence.

## Day 16 Orchestration Boundary

The `e2e` workflow invokes each existing production component once and preserves the intermediate typed results for integration assertions. It does not reimplement evaluator, stability, risk, finding, assessment, or sanitization rules.

The E2E manifest records stage counts, final observed posture, expected safe artifacts, and the raw-evidence export policy.

## Sanitization Boundary

The sanitization step occurs immediately before assessment artifacts are written.

This keeps report construction separate from export safety.

## Data Minimization

Day 13 findings already use a concise evidence summary rather than copying full provider responses into the normalized finding.

Day 15 preserves that design and adds deterministic redaction as another safety layer.

## Safe Export Metadata

`sanitization_summary.json` records which policy ran and how many configured redactions were made.

It also explicitly records:

```text
raw_response_exported = false
raw_prompt_exported = false
```

## Sanitization vs HTML Escaping

Sanitization protects sensitive content.

HTML escaping protects the static HTML renderer from interpreting untrusted report text as markup or script.

They are complementary controls.

## Limitation

Regex rules can only identify patterns they are designed to match.

Safe export therefore reduces exposure risk but does not replace manual report review or broader data-loss-prevention controls.
