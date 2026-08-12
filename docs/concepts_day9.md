# Day 9 Concepts — Real Provider Adapter and Secret-Safe Configuration

## API

API means Application Programming Interface.

Simple meaning:

> One program uses a defined interface to ask another program for a service.

## SDK

SDK means Software Development Kit.

It is a library that makes an API easier to use from Python.

## Provider Adapter

The harness expects:

```text
generate(prompt) → ProviderResponse
```

The adapter converts that into a remote SDK call and converts the returned text back into `ProviderResponse`.

## Environment Variable

An environment variable stores configuration outside Python source code.

Examples:

```text
OPENAI_API_KEY
OPENAI_MODEL
```

## .env vs .env.example

```text
.env
= real local values
= may contain secrets
= NEVER commit

.env.example
= placeholders only
= safe to commit
```

## Secret

A secret is sensitive authentication data such as an API key, password or access token.

## SecretStr

The API key is stored in Pydantic `SecretStr` to reduce accidental display when configuration objects are printed.

## Fail Fast

If the key or model is missing, the provider stops with a clear configuration error before trying a remote request.

## Configuration Precedence

The `.env` loader does not overwrite a value already set by the operating system.

## Responses API

At a high level:

```text
model + prompt
     ↓
Responses API
     ↓
text output
```

The model is configured through `OPENAI_MODEL` rather than hard-coded.

## Timeout

Timeout limits how long a remote operation can wait before being treated as failed.

## Retry

Retry means attempting a temporary failed request again.

## Real vs Mock Provider

Mock providers are predictable and ideal for unit tests and CI.

A real provider is useful for real-world testing, but its output can vary and it may cost money.

## Non-Determinism

A real LLM can phrase the same idea differently across runs.

Therefore exact-string evaluators are less reliable with live models than with deterministic mocks.

## Fake Client Testing

Day 9 unit tests inject a fake client.

That verifies request construction and response conversion without internet access or API credits.

## Key Limitation

Day 9 adds real-provider architecture. It does not yet make the evaluators smart enough for every real-model response.
