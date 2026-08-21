# Day 13 Concepts — Security Findings Model

## Main Goal

Day 13 ka goal:

> Test result ko ek proper security issue record mein convert karna.

## Test Case vs Finding

Test Case:

```text
Hum kya check karna chahte hain?
```

Finding:

```text
Testing ke baad actually kya issue observe hua?
```

Example:

```text
RSK-001 = planned system-prompt leakage test
FND-RSK-001 = observed system-prompt leakage finding
```

## Finding kab banti hai?

Simple Day 13 rule:

```text
Risk Score = 0
→ no finding

Risk Score > 0
→ finding create karo
```

## Security Finding mein kya hota hai?

Important fields:

```text
Finding ID
Source Test ID
Category
Severity
Risk Score
Risk Level
Stability
Status
Observation
Impact
Recommendation
Evidence Summary
```

## Finding ID

Example:

```text
Test ID: RSK-001
Finding ID: FND-RSK-001
```

Is se finding ka source test easily trace ho jata hai.

## Status

Day 13 initial lifecycle:

```text
OPEN
```

Meaning:

> Issue observe hua hai aur ab investigate/remediate karna baqi hai.

Day 13 closure workflow implement nahi karta.

## Observation

Observation batata hai:

> Humne kya observe kiya?

Example:

```text
Test RSK-001 produced 100/100 CRITICAL observed risk.
```

## Impact

Impact batata hai:

> Agar issue real system mein ho to kya problem ho sakti hai?

Example:

System prompt leakage se internal controls expose ho sakte hain.

## Recommendation

Recommendation batati hai:

> Issue ko improve/investigate karne ki direction kya hai?

Recommendation category-specific hoti hai.

## Evidence Summary

Day 13 raw response ko finding mein duplicate nahi karta.

Instead concise metrics rakhta hai:

```text
Issue factor
Pass rate
Stability status
Severity
```

Later Day 15 evidence sanitization ke liye ye cleaner foundation hai.

## Finding != Proof of Full Vulnerability

Finding configured evidence se derived issue record hai.

Iska matlab ye nahi ke:
- every real-world exploit proven hai
- system ka complete security assessment ho gaya
- automated finding human validation ko hamesha replace kar sakti hai

## Day 12 vs Day 13

Day 12:

```text
Issue ko priority number do.
```

Day 13:

```text
Us observed issue ko proper structured finding banao.
```

## Easy Interview Answer

> Day 13 adds a normalized security findings model on top of the risk layer. Non-zero risk records become traceable findings with a deterministic finding ID, source test, category, severity, risk score, stability status, observation, impact, recommendation and concise evidence summary. Zero-risk passing records stay as test evidence and are not incorrectly reported as security findings.
