# Limitations

The AI Red Teaming Test Harness is an educational, defensive security-testing
project. Its results apply only to the configured test packs, providers,
evaluators, scoring rules, and execution environment used for a run.

## Provider Scope

The harness currently supports four provider names:

- `mock-vulnerable`
- `mock-hardened`
- `mock-flaky`
- `openai-live`

The three mock providers are deterministic local simulations. They are useful
for repeatable regression tests, but they do not reproduce the full variability
of production language models.

The optional `openai-live` adapter depends on the configured model, account
access, network availability, provider-side policy, rate limits, and model
updates. Its responses can be non-deterministic and may change without a code
change in this repository.

## Test-Coverage Scope

The included test packs cover configured examples of:

- Prompt leakage
- Prompt injection
- Instruction override
- Refusal behaviour
- Hallucination
- Safety-boundary behaviour
- Benign controls
- Repeated-run stability
- Risk-scoring scenarios

This coverage is not exhaustive. Passing the included cases does not prove that
an AI system is secure against every prompt, language, encoding, multi-turn
strategy, tool call, retrieval source, or model update.

## Evaluator Limitations

The automated evaluators use deterministic checks such as forbidden patterns,
required patterns, regular expressions, response presence, response length,
and refusal-quality signals.

They can miss semantic or context-dependent failures, including:

- Indirect or paraphrased leakage
- Subtle policy violations
- Incorrect but convincing responses
- Multi-turn attacks
- Tool-use or retrieval-layer failures
- Unsafe meaning that does not match a configured pattern

They can also produce false positives. A `REVIEW` verdict means the configured
automation could not make a reliable decision and human review is required.

Day 17 word-scoped literal matching can reduce configured partial-word false
positives, but it does not understand meaning, intent, synonyms, obfuscation,
or language-specific tokenization. Choosing an unsuitable match scope can still
produce false positives or false negatives.

## Stability and Risk Limitations

Stability results describe only the configured number of repeated attempts.
A stable pass over a small sample is not proof that a provider will always
behave safely.

Risk scores are project-specific prioritization values derived from configured
severity, observed issue rate, and stability. They are not CVSS scores and
should not be presented as an industry-standard vulnerability rating.

## Findings and Assessment Limitations

Normalized findings and assessment posture summarize observed non-zero risks
from one configured run. `NO_OBSERVED_FINDINGS` means that no qualifying
finding was produced within that scope. It does not mean that the model or
application is vulnerability-free.

The generated assessment is evidence for review, not a penetration-test
certificate, compliance attestation, or complete security certification.

## Sanitization and Data Handling

The final assessment exporter creates a sanitized copy and does not export full
raw prompts or provider responses in the assessment artifacts. It also applies
HTML escaping to untrusted report text.

Sanitization is regex-based defense in depth. A sensitive value that does not
match a configured rule can still be missed. Earlier execution and diagnostic
artifacts may contain more detailed prompts or responses than the final
assessment report.

Day 17 redacts supported provider exception patterns and bounds their stored
detail. This reduces exposure risk but can also remove diagnostic information;
detailed provider troubleshooting should use access-controlled operational
logs rather than shared assessment artifacts.

The Day 18 top-level showcase summary and manifest intentionally export only
aggregate verdict, posture, finding-count, outcome, and gate evidence. They do
not export raw prompts or provider responses. The in-memory workflow still
processes that evidence, and the nested assessment artifacts remain subject to
the existing regex-based sanitization limitations and manual-review
requirement.

Therefore:

- Use only fictional, public, or explicitly authorized test data.
- Never place real credentials, secrets, or customer data in test packs.
- Keep generated `output/` artifacts out of Git by default.
- Review every artifact before external sharing.
- Store real API keys only in local environment configuration, never in source
  files or screenshots.

## End-to-End Verification Boundary

The Day 16 E2E workflow verifies that the configured loader, provider,
evaluator, stability, risk, findings, assessment, and sanitization components
work together and produce the expected safe artifact set.

A passing E2E run verifies those local pipeline contracts. It does not prove
that every external provider, production deployment, attack technique, or
future model version will behave safely.

## Showcase Boundary

The Day 18 showcase uses deterministic mock providers to demonstrate the
project's workflow in a repeatable way. Four improvements, zero regressions,
and a passed policy gate are expected properties of the included local demo
configuration.

They are not benchmark results for a production model, proof of general risk
reduction, or a security certification. A real assessment requires authorized
targets, representative attack coverage, controlled evidence handling, and
qualified human review.

## Documentation and Portfolio Boundary

Day 19 documentation explains the verified local project behavior and provides
a repeatable recruiter-facing walkthrough. Documentation, badges, diagrams, and
the showcase visual do not add new security coverage or increase the strength
of the underlying evidence.

The included visual reports only the verified deterministic Day 18 values. It
must remain accompanied by its scope disclaimer and must not be presented as a
real-model benchmark, production risk-reduction metric, penetration-test
certificate, or independent audit result.

Repository ignore rules reduce accidental commits but do not protect files
uploaded manually through the GitHub interface. Every uploaded file and image
still requires human review for secrets, raw evidence, private paths, and
personal information.

## Authorized Use Only

This project does not authorize:

- Testing third-party systems without explicit permission
- Credential extraction
- Malware delivery or execution
- Exposure of real customer or employee data
- Automated exploitation of production systems
- Claims of complete or guaranteed AI security

## Future Improvements

Useful next improvements include:

- Calibrated semantic evaluators with explicit human-review fallbacks
- More multi-turn, multilingual, retrieval, and tool-use test scenarios
- Additional provider adapters with timeout and rate-limit telemetry
- Coverage reporting and static-analysis checks in CI
- Versioned test-pack and artifact schemas
- Signed or checksummed assessment manifests for stronger evidence integrity
