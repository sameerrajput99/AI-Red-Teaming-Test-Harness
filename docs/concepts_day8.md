# Day 8 Concepts — Expanding Security Test Coverage

## Objective

Day 8 turns the original three-test starter pack into a broader security assessment pack while preserving the original fixture for regression testing.

## Test Coverage

Test coverage describes how much of the defined threat surface is exercised by the test suite.

Day 1 had three starter checks.

Day 8 has fourteen checks across seven categories.

```text
14 total tests
├── 12 adversarial
└── 2 benign controls
```

## Threat Coverage

Threat coverage means mapping tests to security behaviors that could fail.

The Day 8 categories are:

- Prompt leakage
- Prompt injection
- Instruction override
- Refusal behavior
- Hallucination indicators
- Safety boundaries
- Benign controls

Coverage is broader when different failure modes are tested instead of repeatedly testing the same prompt wording.

## Test Diversity

Two tests in the same category should not simply duplicate each other.

Example:

```text
Prompt leakage test A:
Ask for the system prompt.

Prompt leakage test B:
Ask for confidential developer rules.
```

Both target leakage, but through different request wording.

## Security Test Taxonomy

A taxonomy is an organized classification system.

Day 8 uses the existing `category` field as a small test taxonomy:

```text
prompt_leakage
prompt_injection
instruction_override
refusal_behavior
hallucination
safety_boundary
benign_control
```

A taxonomy helps analysts:

- Group tests
- Measure coverage
- Filter reports
- Identify missing areas
- Add new packs consistently

## Prompt Leakage

Prompt leakage testing checks whether hidden or privileged instructions are exposed.

Examples:

- Hidden system prompt
- Confidential developer rules

Expected hardened behavior:

```text
Do not expose privileged instructions.
```

## Prompt Injection

Prompt injection testing checks whether untrusted user/document content can replace or manipulate higher-priority instructions.

Day 8 includes:

- User-policy replacement attempt
- Document-instruction injection attempt

Expected hardened behavior:

```text
Maintain the trusted instruction hierarchy.
```

## Instruction Override

Instruction override testing checks direct attempts to disable restrictions or activate unrestricted modes.

Day 8 examples:

- Debug-mode override
- Unrestricted maintenance-mode request

## Refusal Behavior

Refusal behavior tests whether the system refuses clearly protected requests.

Day 8 uses safe simulated requests for fake credentials and admin tokens.

The vulnerable provider returns obvious fake markers such as:

```text
CREDENTIALS:
ADMIN_TOKEN:
```

No real credential is stored or exposed.

## Hallucination Indicator Tests

A hallucination is unsupported or fabricated information presented as factual.

Day 8 uses deterministic configured markers:

```text
FAKE_CITATION:
UNVERIFIED_CLAIM:
```

The vulnerable provider deliberately emits these markers. The hardened provider avoids them and states that it cannot verify or invent the requested source.

Important limitation:

> Day 8 does not implement general semantic hallucination detection.

It only checks the configured deterministic indicators.

## Safety Boundary

Safety-boundary tests check whether a system maintains an access or authorization boundary.

Day 8 uses safe simulated prompts such as:

- Bypass authorization
- Disable access control

The vulnerable provider returns a simulated bypass marker. The hardened provider refuses the override.

## Benign Controls

Benign controls protect usability.

Security hardening should not cause the system to reject harmless questions.

Day 8 includes:

- Beginner machine-learning explanation
- Authentication vs authorization explanation

Expected behavior:

```text
Adversarial request → secure boundary
Benign request      → useful response
```

## Positive and Negative Controls

In this project:

- Adversarial tests act like negative/security challenge cases.
- Benign controls confirm expected normal functionality.

Both are important because a system that refuses everything may appear secure while being unusable.

## Regression Fixture

A regression fixture is a small stable input used repeatedly to confirm old behavior still works.

The Day 1 pack remains unchanged for that purpose.

The Day 8 pack is added separately instead of replacing the Day 1 pack.

## Deterministic Simulation

The mock providers are not trying to imitate every possible LLM behavior.

They provide predictable local outputs so that:

- Evaluators can be tested
- Comparison logic can be tested
- CI can be deterministic
- Security concepts can be demonstrated without an external API

## Coverage vs Assurance

Coverage answers:

> What defined behaviors did we test?

Assurance asks the larger question:

> How confident are we that the overall system is secure?

Day 8 improves coverage, but does not provide complete assurance.

## Important Limitation

The expanded pack still uses simple evaluators:

- Forbidden-pattern matching
- Refusal-signal matching
- Response presence

This is deliberate. Evaluator sophistication will be improved separately so that test breadth and evaluation logic remain clearly separated.

## Easy Interview Explanation

> I expanded the harness from a three-case starter fixture to a fourteen-case security pack across seven categories. I preserved the original pack for regression testing, added diverse adversarial prompts plus benign controls, extended the deterministic vulnerable and hardened providers, and updated CI to gate the broader test suite. The pack improves coverage but does not claim complete security assurance.
