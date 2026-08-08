# Architecture Through Day 8

```text
Security Test Pack Library
      ├── Day 1 Starter Pack (3 tests)
      └── Day 8 Expanded Pack (14 tests)
              ↓
        Safe YAML Loader
              ↓
      Pydantic Schema Validation
              ↓
       Validated TestCase Objects
              ↓
           Test Runner
              ↓
        Provider Interface
        ├── Mock Vulnerable
        └── Mock Hardened
              ↓
       Execution Records
              ↓
        Evaluator Engine
        ├── Forbidden Patterns
        ├── Refusal Quality
        └── Response Presence
              ↓
        Security Verdicts
              ↓
      Reports / Comparison
              ↓
        Policy Security Gate
              ↓
         CI/CD Decision
```

## Day 8 Change

Day 8 expands the threat-coverage layer while keeping the core execution architecture stable.

The expanded pack covers seven categories:

1. Prompt leakage
2. Prompt injection
3. Instruction override
4. Refusal behavior
5. Hallucination indicators
6. Safety boundaries
7. Benign controls

Each category currently contains two tests.

## Why the Starter Pack Is Kept

`day1_test_cases.yaml` remains unchanged as a small regression fixture.

`day8_expanded_security_pack.yaml` is a broader assessment pack.

```text
Starter pack = small development/regression fixture
Expanded pack = broader security assessment fixture
```

This avoids rewriting historical evidence while allowing coverage to grow.

## Provider Simulation

The local mock providers use deterministic prompt triggers.

```text
Same prompt
   ↓
Known local response
   ↓
Known evaluator outcome
```

This is useful for:

- Unit testing
- CI
- Demonstrating regressions
- Explaining expected security behavior
- Developing the harness without API cost

The mock providers are simulations, not real language models.

## Coverage vs Assurance

More test cases increase test coverage, but coverage is not the same as complete assurance.

```text
More tests
   ≠
Proof of complete security
```

A test pack can only make claims about the behaviors and evaluators it actually checks.

## Day 8 CI Boundary

The GitHub Actions security gate now executes the expanded pack. A code change that causes one of the defined candidate behaviors to fail can therefore break the CI gate.

## Important Limitation

The current evaluators are intentionally deterministic and relatively simple. Advanced semantic or model-assisted evaluation is not part of Day 8.
