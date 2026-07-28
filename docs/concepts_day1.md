# Day 1 Concepts

## 1. Test Harness

A test harness is the system that organizes, validates, runs and records tests. It is bigger than one test script.

Easy example: a school exam system is the harness. Individual questions are the test cases.

## 2. Test Case

A test case is one clearly defined check. It contains the input, expected behavior, severity and evaluation method.

## 3. Expected Behavior

Expected behavior describes the security property the AI should demonstrate. It is not one exact sentence.

Example: `refuse_and_protect_system_prompt` means the model should refuse and should not reveal hidden instructions, regardless of the exact wording of the refusal.

## 4. Adversarial Test

An adversarial test intentionally tries to make the system fail.

Example: asking the model to ignore previous instructions.

## 5. Benign Control

A benign control is a normal, harmless request. It checks that security controls do not block legitimate use.

A chatbot that refuses everything is not useful or correctly secured.

## 6. Schema Validation

A schema defines what fields and values are allowed. Validation checks the data against that contract before execution.

## 7. Severity

Severity describes the possible security impact if a test fails. It is not the same as how strange a response looks.

## 8. Evaluator

An evaluator checks whether the actual response matches the expected security behavior. On Day 1 we only define evaluator configuration. Evaluator logic will be implemented later.

## 9. Threat Model

A threat model identifies what must be protected, who may attack it, where trust changes and what is in or out of scope.

## 10. Trust Boundary

A trust boundary is a point where data moves between components with different trust levels. Data crossing that point should be validated or treated as untrusted.
