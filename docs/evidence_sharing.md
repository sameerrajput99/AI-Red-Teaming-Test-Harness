# Evidence Sharing Guide

## Objective

Generated security evidence may contain prompts, responses, error details, or
environment information. Share the smallest reviewed artifact set needed for
the audience.

## Recommended Portfolio Files

After manual review, the preferred Day 18 portfolio artifacts are:

```text
showcase_summary.md
showcase_manifest.json
baseline/.../assessment_report.md
candidate/.../assessment_report.md
```

The top-level showcase files are designed to contain aggregate verdict and gate
evidence without raw prompts or provider responses. Assessment reports pass
through the sanitization boundary.

## Do Not Publish by Default

Do not upload these items to GitHub or a public portfolio without a specific,
documented reason and a complete security review:

- `.env` or any credential file
- Raw execution reports
- Raw comparison reports containing provider responses
- Provider error logs
- Customer, employee, or production prompts
- Local output directories copied without review
- Screenshots containing API keys, email addresses, usernames, or private paths

## Pre-Share Checklist

- [ ] Confirm the target system and evidence are authorized for sharing.
- [ ] Search for API keys, bearer tokens, passwords, emails, and private URLs.
- [ ] Confirm raw prompt and raw response export flags are false where expected.
- [ ] Remove local usernames and filesystem paths from screenshots.
- [ ] Confirm the scope statement and limitations remain visible.
- [ ] State that mock-provider results are deterministic simulations.
- [ ] Share only the files required by the audience.

## GitHub Boundary

The repository `.gitignore` excludes `.env`, generated `output/`, virtual
environments, caches, build directories, distributions, and package metadata.
This reduces accidental commits but is not a substitute for reviewing staged or
manually uploaded files.

## Incident Response

If a real secret is published:

1. Revoke or rotate it immediately.
2. Remove it from the current repository state.
3. Assess whether Git history or release artifacts also contain it.
4. Replace affected evidence with sanitized material.
5. Document the incident through an appropriate private channel.

Deleting a visible file alone does not invalidate an exposed credential.
