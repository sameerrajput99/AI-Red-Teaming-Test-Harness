# Day 2 Concepts

## Provider abstraction

A provider adapter is a small layer that knows how to communicate with one chatbot or model configuration. Every provider implements the same `generate(prompt)` contract, so the runner does not need provider-specific code.

```text
Runner → ChatProvider interface → Selected provider
```

This is useful because a local mock, external API, local LLM or RAG application can later be connected without rewriting the runner.

## Mock provider

A mock provider is a controlled local simulation. It is deterministic, requires no API key and cannot target a real system.

- The vulnerable mock intentionally demonstrates weak responses.
- The hardened mock protects internal instructions and answers benign requests.

These names describe configurations, not a security certification of a real model.

## Test runner

The runner is the orchestrator. It:

1. Receives validated test cases.
2. Selects one provider.
3. Sends each prompt to that provider.
4. Measures execution time.
5. Captures response or error.
6. Produces structured execution records.

The runner does not judge security on Day 2.

## Execution status versus security verdict

- **Execution status:** Did the provider call complete? Values: `success` or `error`.
- **Security verdict:** Did the response satisfy the expected security behavior? Future values: `PASS`, `FAIL`, `REVIEW` or `ERROR`.

A vulnerable response can have `execution_status=success` because the provider successfully returned a response, while its future security verdict may be `FAIL`.

## Raw evidence

Raw evidence is the unchanged information captured during execution:

- Run ID
- Test ID
- Provider name
- Prompt
- Response
- Timestamp
- Latency
- Error message, when applicable

Raw evidence should be preserved before evaluation so analysts can review how a verdict was produced.

## Error isolation

One provider failure should become an error record instead of crashing the entire test pack. This allows remaining cases to continue and makes infrastructure failures distinguishable from AI security failures.
