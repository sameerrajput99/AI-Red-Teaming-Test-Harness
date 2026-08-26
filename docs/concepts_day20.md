# Day 20 Concepts — Final QA & v1.0.0 Release

## 1. Day 20 Objective

Day 20 turns the verified Day 1–19 repository into a reproducible `1.0.0`
release. The goal is not to add another evaluator. The goal is to prove that
the complete project is internally consistent, testable, gate-controlled,
buildable, documented, and ready to publish within its honest scope.

## 2. Why Version 1.0.0?

Semantic versioning uses three numbers:

```text
MAJOR.MINOR.PATCH
  1  .  0  .  0
```

- `MAJOR` changes when incompatible public behavior is introduced.
- `MINOR` changes when backward-compatible capability is added.
- `PATCH` changes when backward-compatible fixes are released.

Version `1.0.0` means the project's first defined public release is ready. It
does not mean the software is perfect or security-certified.

## 3. Final QA Layers

Day 20 verifies four different questions:

```text
Regression suite  → Does existing behavior still work?
Security gate     → Does the candidate meet the configured policy?
pip check         → Are installed dependency requirements compatible?
Package build     → Can standard installable artifacts be created?
```

One passing layer cannot replace another. A wheel can build while tests fail,
and tests can pass while version metadata is inconsistent.

## 4. Release Artifacts

`python -m build` creates:

```text
dist/
├── ai_red_teaming_test_harness-1.0.0-py3-none-any.whl
└── ai_red_teaming_test_harness-1.0.0.tar.gz
```

The wheel is a built Python package. The source distribution contains the
source release used by packaging tools. Both are generated artifacts, so the
source repository ignores `build/` and `dist/`.

## 5. Changelog vs Release Notes

The changelog is the long-term version history. Release notes are the focused
description shown to users for one release.

```text
CHANGELOG.md              → all important versions and milestones
RELEASE_NOTES_v1.0.0.md   → only the 1.0.0 release
```

## 6. Git Tag vs GitHub Release

A Git tag gives a permanent name such as `v1.0.0` to one verified commit. A
GitHub release is a page built around that tag with release notes and optional
downloadable artifacts.

The tag must point to the exact commit whose tests, gate, and build were
verified. A published tag should not be silently moved to different code.

## 7. Six Release-Readiness Tests

The new tests verify:

1. Version metadata agrees on `1.0.0`.
2. Required Day 20 release documents exist.
3. README relative links still resolve.
4. Changelog and release notes preserve verified scope.
5. CI runs tests, the security gate, dependency checks, and package build.
6. Packaging metadata and artifact ignore rules are release-safe.

Expected regression result:

```text
Day 19 = 114 passed
Day 20 = 120 passed
```

## 8. Release Evidence Is Not Certification

`120 passed` proves that the automated regression contracts passed in the
verified environment. `Gate status: PASSED` proves that the configured
candidate satisfied the configured policy for the configured test pack.

Neither statement proves that every real model, application, language,
multi-turn attack, tool call, retrieval source, or future update is secure.

## 9. Final Project Explanation

> I built a Python AI red-teaming test harness that converts structured YAML
> scenarios into repeatable provider executions, deterministic verdicts,
> stability and risk evidence, normalized findings, sanitized reports, and a
> policy gate. The final release has 120 automated tests, a complete E2E path,
> a reproducible local showcase, and documented security and evidence-sharing
> boundaries. Its claims remain limited to the configured assessment scope.
