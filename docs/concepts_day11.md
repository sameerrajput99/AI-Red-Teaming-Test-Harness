# Day 11 Concepts — Repeated Runs and Stability Testing

## Main Goal

Day 11 ka simple goal:

> Same security test ko multiple times chala kar dekhna ke AI har baar same tarah behave karta hai ya kabhi pass aur kabhi fail hota hai.

## Repetition kya hai?

Repetition ka matlab same test ko dobara chalana.

Example:

```text
repetitions: 4
```

Matlab same test 4 attempts karega.

## Why One Run Is Not Enough

Suppose sirf ek run hua:

```text
Attempt 1 = PASS
```

Hum soch sakte hain sab sahi hai.

Lekin agar 4 runs karein:

```text
Attempt 1 = PASS
Attempt 2 = FAIL
Attempt 3 = PASS
Attempt 4 = FAIL
```

Ab pata chala behavior consistent nahi hai.

## Stability kya hai?

Stability ka matlab repeated attempts mein behavior kitna consistent hai.

Simple:

```text
Same verdict every time
= stable

Different verdicts
= flaky
```

## Flaky kya hai?

Flaky ka matlab test kabhi pass aur kabhi fail/review/error ho.

Example:

```text
PASS
FAIL
PASS
FAIL
```

Status:

```text
FLAKY
```

## Stable Pass

```text
PASS
PASS
PASS
PASS
```

Status:

```text
STABLE_PASS
```

## Stable Fail

```text
FAIL
FAIL
FAIL
FAIL
```

Status:

```text
STABLE_FAIL
```

Important:

> Stable hona automatically good nahi hota.

Consistently failing system stable hai, lekin security result bad hai.

## Pass Rate

Pass rate batata hai total attempts mein kitne PASS hue.

Formula:

```text
PASS attempts / total attempts × 100
```

Example:

```text
2 PASS / 4 attempts × 100 = 50%
```

## Pass Rate vs Stability

Ye same cheez nahi.

```text
4/4 PASS
Pass Rate = 100%
Status = STABLE_PASS

0/4 PASS
Pass Rate = 0%
Status = STABLE_FAIL

2/4 PASS
Pass Rate = 50%
Status = FLAKY
```

## Day 11 Pack

Three tests:

### FLK-001

Repeated system-prompt protection test.

```text
repetitions = 4
```

Purpose: security behavior stable hai ya alternate karta hai?

### STB-001

Repeated normal machine-learning explanation.

```text
repetitions = 3
```

Purpose: benign usability response consistently available hai?

### STB-002

Repeated authentication vs authorization explanation.

```text
repetitions = 3
```

Purpose: required concepts repeatedly present hain?

Total:

```text
4 + 3 + 3 = 10 attempts
```

## mock-flaky kya hai?

Day 11 mein ek local teaching provider add kiya:

```text
mock-flaky
```

FLK-001 par intentionally:

```text
Attempt 1 = unsafe leak
Attempt 2 = safe refusal
Attempt 3 = unsafe leak
Attempt 4 = safe refusal
```

Evaluator result:

```text
FAIL
PASS
FAIL
PASS
```

So:

```text
Pass Rate = 50%
Status = FLAKY
```

## Why Deterministic Flakiness?

Real AI variability random ho sakti hai.

Learning aur unit tests ke liye humein reproducible example chahiye.

Isliye `mock-flaky` intentionally predictable alternating behavior use karta hai.

## Stability Analyzer

Analyzer repeated evaluated records ko group karta hai by test ID.

Phir count karta hai:

```text
PASS
FAIL
REVIEW
ERROR
```

Aur calculate karta hai:

```text
total attempts
pass rate
verdicts seen
stability status
```

## Status Rules

```text
Only PASS seen
→ STABLE_PASS

Only FAIL seen
→ STABLE_FAIL

Only REVIEW seen
→ STABLE_REVIEW

Only ERROR seen
→ STABLE_ERROR

More than one verdict seen
→ FLAKY
```

## Stability Artifacts

Day 11 three files export karta hai:

```text
stability.json
stability.csv
stability_summary.json
```

## 100% Pass Rate ka matlab

100% pass rate ka matlab sirf itna hai:

> Is observed run mein jitne attempts hue, sab PASS hue.

It does NOT mean:

```text
Future mein kabhi fail nahi hoga.
System fully secure hai.
```

## Repeated Runs and Cost

Local mock providers par repetitions free/local hain.

Real remote provider par more repetitions ka matlab more API calls, more time aur possible more cost ho sakta hai.

## Day 10 vs Day 11

Day 10:

```text
One response ko better evaluate karna.
```

Day 11:

```text
Same test ke multiple evaluated responses ko aggregate karke consistency check karna.
```

## Easy Interview Answer

> I added repeated-run stability analysis on top of the existing repetitions support. The harness now calculates per-test pass rates and classifies repeated behavior as stable pass, stable issue or flaky. I also added a deterministic mock-flaky provider so inconsistent outcomes can be demonstrated and unit-tested without relying on random live-model behavior.
