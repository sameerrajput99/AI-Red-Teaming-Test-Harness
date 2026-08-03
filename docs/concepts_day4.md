# Day 4 Concepts: Evidence Reporting

## 1. Reporter

A reporter converts evaluated Python objects into a file format that people or tools can use.

```text
EvaluatedRecord Objects → Reporter → File Artifact
```

## 2. Serialization

Serialization means converting an in-memory object into a storable or transferable format such as JSON.

```text
Python Object → JSON Text
```

Deserialization is the reverse process.

## 3. JSON Report

JSON preserves nested structure. One test result can contain its execution record, final verdict and multiple evaluator findings.

Best uses:

- Automation
- APIs
- Later HTML/PDF generation
- Detailed evidence review

## 4. CSV Report

CSV is a flat table. Each evaluated execution becomes one row.

Best uses:

- Excel or Google Sheets
- Filtering
- Sorting
- Quick analyst review

Nested findings must be flattened into text columns because CSV does not naturally store nested objects.

## 5. Flattening

Flattening converts nested data into simple columns.

```text
findings = [finding 1, finding 2]
```

becomes:

```text
evaluator_types = forbidden_patterns | refusal_quality
```

Flattening improves table readability but loses some nested structure. This is why both JSON and CSV are generated.

## 6. Artifact

An artifact is a file produced by a testing run, such as:

- `results.json`
- `results.csv`
- `summary.json`

Artifacts are evidence, not just terminal output.

## 7. Run Summary

A run summary contains aggregated metrics:

- Total tests
- PASS count
- FAIL count
- REVIEW count
- ERROR count
- Average latency

It does not replace detailed evidence.

## 8. Aggregation

Aggregation combines many individual records into overall metrics.

```text
3 individual verdicts → PASS=1, FAIL=2
```

## 9. Audit Trail

An audit trail allows a reviewer to trace a result back to its source:

```text
Summary → Detailed Result → Raw Response → Prompt → Test ID → Run ID
```

## 10. Evidence Integrity

Reports should preserve exact prompts, responses, timestamps and findings. Editing evidence after a run can make results unreliable.

Day 4 does not yet add cryptographic hashes or signatures. Those can be added later.

## 11. Output Directory per Run

Each run receives a separate directory named with its `run_id`.

This prevents evidence from different test sessions from being mixed or overwritten.

## 12. Machine-Readable vs Human-Reviewable

JSON is highly machine-readable.

CSV is convenient for human analysts and spreadsheets.

A professional testing tool often produces more than one format because different consumers need different representations.

## 13. Sensitive Evidence

Reports may contain model responses and prompts. In a real assessment they could include sensitive content. Therefore:

- Do not commit real generated evidence containing secrets
- Do not use real private data in local simulations
- Share reports only with authorized people
- Keep sanitized samples separately

## One-Line Day 4 Summary

Day 4 converts evaluated AI security results into traceable JSON, CSV and summary artifacts that can be reviewed, analyzed and reused.
