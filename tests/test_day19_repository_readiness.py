"""Day 19 repository and documentation readiness tests."""

from __future__ import annotations

import re
from pathlib import Path

import ai_red_teaming_harness


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_package_version_metadata_is_consistent() -> None:
    pyproject = _read("pyproject.toml")
    version_match = re.search(r'^version = "([^"]+)"$', pyproject, re.MULTILINE)

    assert version_match is not None
    assert ai_red_teaming_harness.__version__ == version_match.group(1)


def test_required_repository_documents_exist() -> None:
    required = (
        "SECURITY.md",
        "CONTRIBUTING.md",
        "DAY19_CHECKLIST.md",
        "docs/concepts_day19.md",
        "docs/demo_walkthrough.md",
        "docs/interview_guide.md",
        "docs/evidence_sharing.md",
        "docs/assets/day18_showcase_result.svg",
    )

    assert all((PROJECT_ROOT / path).is_file() for path in required)


def test_readme_relative_links_resolve_to_repository_files() -> None:
    readme = _read("README.md")
    targets = re.findall(r"!?\[[^]]*]\(([^)]+)\)", readme)
    relative_targets = [
        target.split("#", maxsplit=1)[0]
        for target in targets
        if target and not target.startswith(("http://", "https://", "#"))
    ]

    assert relative_targets
    assert all((PROJECT_ROOT / target).exists() for target in relative_targets)


def test_security_and_evidence_guides_protect_sensitive_data() -> None:
    security = _read("SECURITY.md")
    evidence = _read("docs/evidence_sharing.md")

    assert "Do not open a public issue containing secrets" in security
    assert "explicit written authorization" in security
    assert "Do Not Publish by Default" in evidence
    assert "Revoke or rotate it immediately" in evidence


def test_gitignore_excludes_local_secrets_and_generated_artifacts() -> None:
    gitignore = _read(".gitignore")

    for required_rule in (".env", ".venv/", "output/*", "build/", "dist/"):
        assert required_rule in gitignore


def test_showcase_visual_uses_verified_scoped_values() -> None:
    visual = _read("docs/assets/day18_showcase_result.svg")

    assert "4 IMPROVED" in visual
    assert "0 REGRESSED" in visual
    assert "1 UNCHANGED PASS" in visual
    assert "GATE PASSED" in visual
    assert "not a production security certification" in visual
