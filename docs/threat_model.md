# Threat Model

## Project Scope

The AI Red Teaming Test Harness is a safe local framework for organizing and executing authorized AI security tests.

## Protected Assets

- Test-case integrity
- Expected security behavior
- Raw model responses
- Generated evidence and reports
- Future API credentials
- Hidden system instructions used in controlled simulations

## Threat Actors

- A malicious user attempting prompt manipulation
- A careless tester creating invalid test cases
- A poisoned document or untrusted external input
- A misconfigured chatbot or provider
- An unauthorized person trying to access saved evidence

## Trust Boundaries

```text
Test Pack | Harness | Provider/Chatbot | Evaluator | Evidence Storage
```

Data crossing each boundary must be validated or treated as untrusted.

## In Scope for Version 1

- Prompt leakage
- Prompt injection
- Instruction override
- Refusal behavior
- Hallucination scenarios
- Safety-boundary scenarios
- Vulnerable versus hardened local configurations
- Structured evidence generation

## Out of Scope

- Unauthorized testing of production systems
- Real private data
- Real credential extraction
- Malware execution
- Claims that a model is fully secure
- Automated exploitation of third-party systems

## Day 1 Risks and Controls

| Risk | Control |
|---|---|
| Invalid or incomplete test case | Strict Pydantic schema |
| Unexpected YAML object construction | `yaml.safe_load()` |
| Unknown fields silently accepted | `extra="forbid"` |
| Empty prompts or descriptions | String validation |
| Unsupported category or severity | Enum validation |
