# Architecture Through Day 5

```text
YAML Test Pack
      ↓
Safe YAML Loader
      ↓
Pydantic Schema Validation
      ↓
Validated TestCase Objects
      ↓
Test Runner
      ↓
ChatProvider Interface
      ├── Mock Vulnerable Configuration (baseline)
      └── Mock Hardened Configuration (candidate)
      ↓
ExecutionRecord
      ↓
Evaluator Engine
      ├── Forbidden Patterns
      ├── Refusal Quality
      └── Response Presence
      ↓
EvaluatedRecord
      ├── RunSummary and Run Reports
      │       ├── results.json
      │       ├── results.csv
      │       └── summary.json
      │
      └── Comparison Engine
              ↓
        Align by Test ID + Attempt
              ↓
        ComparisonRecord
              ↓
        ComparisonSummary
              ↓
        Comparison Writers
              ├── comparison.json
              ├── comparison.csv
              └── comparison_summary.json
```

## Component Responsibilities

| Component | Responsibility |
|---|---|
| Loader | Safely parse YAML data |
| Schema | Reject invalid test definitions |
| Runner | Execute validated tests and capture raw evidence |
| Provider | Connect the runner to one chatbot configuration |
| Evaluator | Judge one response against one configured rule |
| Evaluation engine | Combine findings into a final security verdict |
| Run reporters | Persist evidence for one provider run |
| Comparison engine | Align equivalent tests and classify security change |
| Comparison summary | Aggregate improved, regressed and unchanged outcomes |
| Comparison writers | Export side-by-side evidence to JSON and CSV |

## Comparison Invariants

A valid comparison requires:

1. The same validated test pack on both sides.
2. One baseline provider and one different candidate provider.
3. Matching test IDs on both sides.
4. The same number of attempts for each test ID.
5. Raw responses and verdicts preserved for auditability.

If the record sets do not align, the comparison workflow stops with a clear error instead of silently comparing unrelated evidence.

## Trust Boundaries

1. Test pack to loader
2. Validated objects to runner
3. Runner to each provider
4. Provider output to evaluators
5. Evaluated evidence to comparison engine
6. Comparison records to local artifact storage

Comparison artifacts can contain complete prompts and raw responses. They must be treated as security evidence and should not contain real secrets or unauthorized private data.
