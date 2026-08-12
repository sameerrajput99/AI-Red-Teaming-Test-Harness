# Day 10 Checklist — Advanced Evaluators

## Setup
- [ ] Merge Day 10 update into Day 9 project
- [ ] Replace models.py
- [ ] Replace evaluator factory and engine
- [ ] Add three new evaluator files
- [ ] Add Day 10 demo pack
- [ ] Reinstall package
- [ ] Confirm version `0.10.0`

## Validation
- [ ] Run `validate-ai-tests test_packs/day10_advanced_evaluator_pack.yaml`
- [ ] Confirm 4 tests validate

## Vulnerable
- [ ] Evaluate mock-vulnerable
- [ ] Confirm PASS=2
- [ ] Confirm FAIL=2
- [ ] Confirm REVIEW=0
- [ ] Confirm ERROR=0

## Hardened
- [ ] Evaluate mock-hardened
- [ ] Confirm PASS=4
- [ ] Confirm FAIL=0
- [ ] Confirm REVIEW=0
- [ ] Confirm ERROR=0

## Regression
- [ ] Run `python -m pytest`
- [ ] Confirm `55 passed`
- [ ] Confirm Day 8 expanded pack still works
- [ ] Confirm Day 8 security gate still passes

## Theory
- [ ] Explain exact string vs regex
- [ ] Explain regex_forbidden
- [ ] Explain required_patterns
- [ ] Explain match_mode any vs all
- [ ] Explain case sensitivity
- [ ] Explain response_length
- [ ] Explain composite precedence
- [ ] Explain false positive
- [ ] Explain false negative
- [ ] Explain why deterministic evaluator is not full semantic understanding
