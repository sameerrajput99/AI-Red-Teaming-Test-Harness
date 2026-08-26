# Security Policy

## Supported Version

Security fixes are applied to the current development line:

| Version | Supported |
| --- | --- |
| `1.0.x` | Yes |
| Earlier versions | Upgrade before reporting reproducibility issues |

## Reporting a Vulnerability

Do not open a public issue containing secrets, private prompts, provider
responses, credentials, exploit details, or customer data.

Use GitHub private vulnerability reporting when it is enabled for this
repository. If a private reporting channel is not available, open a minimal
public issue asking the maintainer for a secure contact method. Do not include
technical exploit details in that issue.

Please include only the information needed to reproduce the problem safely:

- Affected version or commit
- Affected component or command
- Security impact within the harness scope
- Minimal reproduction using fictional data
- Whether the issue exposes stored or exported evidence
- A safe proposed remediation, if known

Do not test a suspected issue against third-party or production systems without
explicit written authorization.

## Secret Handling

- Never commit `.env`, API keys, bearer tokens, passwords, or private test data.
- Use fictional values in test packs and regression tests.
- Treat generated execution and comparison evidence as potentially sensitive.
- Review sanitized assessment and showcase artifacts before sharing them.
- Revoke and rotate a real secret immediately if it is exposed.

## Scope

This policy covers vulnerabilities in the test harness itself, including its
loading, provider, evaluation, reporting, sanitization, and evidence-handling
boundaries.

It does not authorize security testing of AI providers, websites, APIs, or
other systems that you do not own or have explicit permission to assess.
