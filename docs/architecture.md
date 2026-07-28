# Day 1 Architecture

## Current Flow

```text
Test Author
    |
    v
YAML Test Pack
    |
    v
safe_load()
    |
    v
Python dictionaries
    |
    v
Pydantic TestCase validation
    |
    +--> Valid: create typed TestCase objects
    |
    +--> Invalid: stop and show exact validation errors
```

## Why Validation Comes First

A test runner should not execute incomplete or ambiguous tests. Validation ensures every test has:

- A unique-style identifier
- A title and description
- A recognized category
- A prompt
- A defined expected behavior
- A severity
- At least one evaluator

## Planned Components

```text
Test Packs → Loader → Validator → Runner → Provider → Evaluators → Evidence → Reports
```

Only the Loader and Validator are implemented on Day 1.
