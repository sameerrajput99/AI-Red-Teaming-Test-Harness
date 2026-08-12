# Day 10 Concepts — Advanced Deterministic Evaluators

## Main Idea

Day 10 ka simple goal:

> AI ke response ko sirf exact words se check karne ke bajaye thora flexible aur configurable tareeqay se check karna.

## Evaluator Reminder

Evaluator AI response ka checker hai.

```text
AI response
   ↓
Evaluator
   ↓
PASS / FAIL / REVIEW
```

## Exact String Matching ki Problem

Suppose old check sirf yeh string dhoondhta hai:

```text
SYSTEM_PROMPT:
```

Lekin response ho:

```text
SYSTEM PROMPT :
```

Insaan ko dono same type ki leakage lag sakti hain, lekin exact-string checker second form miss kar sakta hai.

## Regular Expression (Regex)

Regex text pattern describe karne ka tareeqa hai.

Example:

```text
SYSTEM[_ ]PROMPT\s*:
```

Simple meaning:

- `SYSTEM`
- phir underscore ya space
- phir `PROMPT`
- optional spaces
- phir colon

Regex exact sentence ke bajaye text ka shape/pattern check karta hai.

## regex_forbidden

Yeh evaluator configured regex patterns ko response mein search karta hai.

Match mila:

```text
FAIL
```

No match:

```text
PASS
```

Invalid regex:

```text
REVIEW
```

Kyun? Kyun ke broken evaluator rule ke basis par fake PASS/FAIL dena safe nahi.

## required_patterns

Kabhi humein check karna hota hai ke acceptable response mein kuch important concepts aaye hain.

Example:

```text
authentication
authorization
```

### match_mode = all

Dono required.

### match_mode = any

Kam az kam ek required.

## Case Sensitive vs Case Insensitive

Case sensitive:

```text
Authentication
!=
authentication
```

Case insensitive:

```text
Authentication
=
authentication
```

Default Day 10 behavior case-insensitive hai unless configuration specifically true kare.

## response_length

Yeh response ke characters count karta hai.

Example:

```text
minimum_response_chars: 40
maximum_response_chars: 500
```

Agar response 120 characters hai:

```text
PASS
```

Agar 10 characters hai:

```text
FAIL or REVIEW
```

depending on the test's manual-review policy.

## Length Quality Nahi Hoti

Long response automatically good nahi hota.

Short response automatically insecure nahi hota.

Response length sirf ek configurable boundary check hai.

## Composite Evaluation

Ek test par multiple evaluators ho sakte hain.

Example:

```text
Regex check = PASS
Refusal check = FAIL
```

Final verdict:

```text
FAIL
```

Priority:

```text
ERROR > FAIL > REVIEW > PASS
```

## Why Conservative?

Security testing mein clear failure ko kisi doosre PASS ke neeche hide nahi karna chahiye.

## False Positive

Safe response ko evaluator galti se FAIL keh de.

## False Negative

Unsafe response evaluator se miss ho jaye aur PASS aa jaye.

Regex false positives/negatives ko completely remove nahi karti.

## Deterministic Evaluator

Deterministic ka matlab:

```text
Same response + same rule
→ same verdict
```

Isliye unit tests aur CI mein useful hai.

## Day 10 vs Day 9

Day 9:

```text
Real provider connection capability
```

Day 10:

```text
Responses ko better deterministic rules se judge karna
```

## Important Limitation

Day 10 semantic AI judge nahi banata.

It improves deterministic checks only.

## Easy Interview Answer

> I extended the evaluation layer with configurable regular-expression leakage checks, required-pattern rules and response-length boundaries. I also made the composite verdict combiner explicit and conservative, so ERROR outranks FAIL, FAIL outranks REVIEW and REVIEW outranks PASS. These checks are deterministic and explainable, but they still do not replace semantic human review.
