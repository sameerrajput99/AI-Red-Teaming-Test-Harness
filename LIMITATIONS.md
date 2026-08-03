# Limitations

The AI Red Teaming Test Harness is an educational and defensive security-testing project.

Its results must be interpreted only within the scope of the configured test cases, mock providers and evaluator rules.

## Current Provider Scope

The current implementation uses two deterministic local mock providers:

- `mock-vulnerable`
- `mock-hardened`

These providers simulate vulnerable and hardened chatbot behaviour.

They are not real production language models and do not represent the full variability of deployed LLM systems.

## Current Test Coverage

The current starter test pack contains:

- Direct system-prompt leakage
- Direct instruction override
- One benign usability control

Additional categories are planned, including:

- Prompt injection
- Refusal behaviour
- Hallucination
- Safety-boundary testing

These categories should not be treated as fully implemented until corresponding test cases and evaluators are added.

## Evaluator Limitations

The current evaluators use checks such as:

- Forbidden-pattern detection
- Refusal-signal detection
- Response-presence validation

These evaluators may miss:

- Semantic leakage
- Indirect disclosures
- Context-dependent unsafe behaviour
- Subtle policy violations
- Incorrect but convincing responses

They may also produce false positives when safe responses contain words similar to configured failure patterns.

## Verdict Interpretation

The harness currently uses:

- `PASS`
- `FAIL`
- `REVIEW`
- `ERROR`

A `PASS` means the response passed the configured checks for that test.

It does not prove that the AI system is completely secure.

A `REVIEW` result means automated checks could not reach a reliable conclusion and human review is required.

An `ERROR` means execution or evaluation failed.

## Comparison Limitations

The comparison results apply only to:

- The same configured test pack
- The selected mock providers
- The current evaluator rules

An `IMPROVED` result does not mean the hardened configuration is fully secure.

It only means its result was safer than the baseline result for the same configured test.

## Data Handling

Generated evidence may contain complete prompts and raw responses.

Only fictional, public or explicitly authorised data should be used.

Do not include:

- Passwords
- API keys
- Private customer data
- Real credentials
- Unauthorised third-party information

## Out of Scope

This project does not authorise:

- Testing third-party systems without permission
- Credential extraction
- Malware execution
- Real customer-data exposure
- Automated exploitation
- Complete security certification
- Claims of 100% prompt-injection protection

## Planned Improvements

Future improvements include:

- More structured adversarial test cases
- Additional evaluator types
- False-positive analysis
- Repeated test runs
- Sanitised example evidence
- Optional real-model adapters
- Improved security reports
- Automated GitHub testing
