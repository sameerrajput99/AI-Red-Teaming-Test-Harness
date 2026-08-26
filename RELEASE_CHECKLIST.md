# Release Checklist

Use this checklist for version `1.0.0` and future releases.

## 1. Prepare

- Confirm the intended version follows semantic versioning.
- Update `pyproject.toml` and `src/ai_red_teaming_harness/__init__.py`.
- Update README status, expected test count, changelog, release notes, and supported version.
- Confirm no real secret, raw private evidence, or personal path is present.

## 2. Verify

Run from an activated project virtual environment:

```powershell
python -m pip install -e ".[dev]"
python -m pytest
gate-ai-tests test_packs/day8_expanded_security_pack.yaml `
  --policy policies/strict_gate.yaml `
  --baseline mock-vulnerable `
  --candidate mock-hardened
python -m pip check
python -m build
```

For version `1.0.0`, the expected results are:

```text
120 tests passed
Gate status: PASSED
No broken requirements found
dist/ai_red_teaming_test_harness-1.0.0-py3-none-any.whl
dist/ai_red_teaming_test_harness-1.0.0.tar.gz
```

## 3. Review

- Check the GitHub Actions run on the final `main` commit.
- Open README links and inspect the rendered SVG.
- Review all changed files and the distribution filenames.
- Keep `.env`, `.venv`, caches, `output/`, `build/`, `dist/`, and `*.egg-info` out of the source upload.
- Re-read `LIMITATIONS.md`, `SECURITY.md`, and the release notes.

## 4. Publish on GitHub

1. Open the repository's **Releases** page.
2. Select **Draft a new release**.
3. Create the tag `v1.0.0` from the verified `main` branch.
4. Use the title `AI Red Teaming Test Harness v1.0.0`.
5. Paste the reviewed contents of `RELEASE_NOTES_v1.0.0.md`.
6. Attach the wheel and source distribution only if you want downloadable package artifacts.
7. Confirm the scope disclaimer remains visible, then publish.

## 5. After Publication

- Open the tag and release links in a private browser window.
- Confirm the attached filenames and version are correct.
- Preserve the passing workflow URL as release evidence.
- Never replace a published tag with different code; create a new patch version instead.
