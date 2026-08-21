# Day 15 Concepts — Evidence Sanitization & Safe Export

## Main Goal

Day 15 ka goal:

> Security report share karne se pehle sensitive evidence ko redact karna.

## Sanitization kya hai?

Sanitization ka simple matlab:

> Sensitive text ko safe placeholder se replace karna.

Example:

```text
API_KEY=MYSECRET123
```

becomes:

```text
API_KEY=[REDACTED_SECRET]
```

## Redaction kya hai?

Redaction = sensitive value hide karna.

Example:

```text
analyst@example.com
→ [REDACTED_EMAIL]
```

## Day 15 kya detect karta hai?

Default policy:

```text
OpenAI-style sk- keys
Bearer tokens
generic API key / secret / token / password assignments
email addresses
```

## Safe Export kya hai?

Report ko direct raw form mein write nahi karna.

Flow:

```text
Report
→ Sanitize
→ Export
```

## Data Minimization

Jitni information report ko actually chahiye sirf utni export karo.

Day 15 final assessment full raw prompt aur raw model response export nahi karta.

Instead concise metrics/evidence summary use hoti hai.

## sanitization_summary.json

Ye batata hai:

```text
Kaunsi policy run hui?
Kitni redactions hui?
Kis rule ne kitni values redact ki?
Raw prompt export hua? false
Raw response export hua? false
```

## Sanitization vs HTML Escaping

Dono different hain:

```text
Sanitization
= secret hide karta hai

HTML Escaping
= text ko executable HTML/script banne se rokta hai
```

## Important Limitation

Regex sanitizer perfect nahi hota.

Agar secret unusual format mein ho aur rule match na kare, wo miss ho sakta hai.

Isliye:

> Automated sanitization + manual review

best approach hai.

## Easy Interview Answer

> Day 15 adds a deterministic sanitization layer immediately before assessment export. It redacts configured sensitive patterns such as API keys, bearer tokens, generic secrets and email addresses, preserves HTML escaping, avoids exporting raw prompts/responses in the final assessment, and writes a sanitization summary for auditability.
