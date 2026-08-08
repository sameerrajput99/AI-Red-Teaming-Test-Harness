# Day 7 Concepts — Security Policy Gate and CI/CD

## Objective

Day 7 converts comparison evidence into an automated decision. Instead of only displaying improvements and regressions, the harness now applies an explicit YAML policy and returns a process exit code.

## Security Gate

A security gate is a checkpoint that decides whether a candidate configuration satisfies defined security conditions.

```text
Comparison results
       ↓
Security policy
       ↓
Gate rules
       ↓
PASSED or FAILED
```

The gate does not guess what “secure enough” means. The policy defines the acceptable thresholds.

## Policy as Code

Policy as Code means writing governance or security rules in a version-controlled, machine-readable file.

Example:

```yaml
max_regressed: 0
max_candidate_failures: 0
minimum_improvements: 2
```

Benefits:

- Rules are explicit
- Rules can be reviewed
- Rules can be versioned
- The same rules run locally and in CI
- Decisions become repeatable
- Changes leave an audit trail

## Threshold

A threshold is an allowed numerical limit.

```text
Observed regressions = 0
Maximum regressions  = 0
Result               = PASS
```

Another example:

```text
Observed failures = 1
Maximum failures  = 0
Result            = FAIL
```

## Rule Result

Each policy condition produces an individual rule result containing:

- Rule identifier
- Whether it passed
- Observed value
- Expected condition
- Human-readable reason

A final gate fails when at least one required rule fails.

## Gate Status

### PASSED

All policy rules passed.

### FAILED

The comparison completed, but one or more policy rules failed.

A failed gate is a valid security decision, not necessarily a software error.

## Exit Code

A process exit code is a small integer returned by a command to the operating system.

```text
0 = success
1 = policy failure
2 = operational/configuration error
```

CI systems use exit codes to decide whether a job should continue or stop.

## Gate Failure vs Execution Error

```text
Gate failure:
Tests ran correctly, but policy was not satisfied.

Execution error:
The tool could not complete because a file, schema, provider or process failed.
```

Keeping these states separate improves troubleshooting.

## CI/CD

CI means Continuous Integration. It automatically checks changes when code is pushed or a pull request is opened.

CD may mean Continuous Delivery or Continuous Deployment. It moves validated changes toward release.

Day 7 focuses on a CI security check:

```text
Code push or pull request
          ↓
Install project
          ↓
Run unit tests
          ↓
Run AI security gate
          ↓
Pass or block
```

## GitHub Actions

GitHub Actions is the automation runner used by the included workflow.

The workflow runs the deterministic local test harness. It does not call a production model and does not require an API key.

## Fail Closed

Fail closed means the system does not silently approve a candidate when required evidence is missing or a policy rule fails.

Examples:

- Candidate errors exceed the allowed threshold
- Record sets do not align
- Policy file is invalid
- A regression is detected

The workflow stops instead of claiming success.

## Benign-Control Regression

A security fix can accidentally block legitimate behavior.

```text
Baseline benign test  = PASS
Candidate benign test = FAIL
Outcome               = REGRESSED
```

The `require_no_benign_regressions` rule protects usability as well as attack resistance.

## Auditability

The gate writes `gate_result.json`, which includes:

- Policy identity
- Gate status
- Comparison identity
- Every rule result
- Observed values
- Expected thresholds
- Decision reasons
- Generation timestamp

This allows a reviewer to understand why the gate passed or failed.

## Deterministic Gate

The gate engine evaluates already produced counts and outcomes with fixed rules. It does not use another LLM to make the final decision.

This makes the gate:

- Repeatable
- Explainable
- Testable
- Suitable for automation

## Important Limitation

A passed gate means:

> The candidate satisfied this policy for this test pack and these evaluators.

It does not mean:

> The complete AI system is fully secure.

## Easy Interview Explanation

> I added a policy-as-code security gate that evaluates baseline-versus-candidate comparison evidence against strict YAML thresholds. It produces explainable rule-level results, writes a machine-readable gate artifact, and returns distinct process exit codes for policy failure and operational errors. I also added a GitHub Actions workflow so unit tests and the security gate run automatically on repository changes.
