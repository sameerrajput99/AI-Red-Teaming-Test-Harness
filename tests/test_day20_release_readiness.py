"""Day 20 final release-readiness tests."""

from __future__ import annotations

import re
from pathlib import Path

import ai_red_teaming_harness


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_day20_release_version_is_consistent() -> None:
    assert 'version = "1.0.0"' in _read("pyproject.toml")
    assert ai_red_teaming_harness.__version__ == "1.0.0"
    assert "Package version | `1.0.0`" in _read("README.md")
    assert "| `1.0.x` | Yes |" in _read("SECURITY.md")


def test_day20_release_documents_exist() -> None:
    required = (
        "DAY20_CHECKLIST.md",
        "CHANGELOG.md",
        "RELEASE_CHECKLIST.md",
        "RELEASE_NOTES_v1.0.0.md",
        "docs/concepts_day20.md",
        "docs/portfolio_showcase.md",
    )

    assert all((PROJECT_ROOT / path).is_file() for path in required)


def test_day20_readme_relative_links_resolve() -> None:
    readme = _read("README.md")
    targets = re.findall(r"!?\[[^]]*]\(([^)]+)\)", readme)
    relative_targets = [
        target.split("#", maxsplit=1)[0]
        for target in targets
        if target and not target.startswith(("http://", "https://", "#"))
    ]

    assert relative_targets
    assert all((PROJECT_ROOT / target).exists() for target in relative_targets)


def test_day20_release_notes_preserve_verified_scope() -> None:
    changelog = _read("CHANGELOG.md")
    release_notes = _read("RELEASE_NOTES_v1.0.0.md")

    assert "## [1.0.0]" in changelog
    assert "Days 1–3" in changelog
    assert "Day 20" in changelog
    assert "120 passed" in release_notes
    assert "Configured AI security gate   PASSED" in release_notes
    assert "not a benchmark for a production model" in release_notes


def test_day20_ci_verifies_tests_gate_dependencies_and_build() -> None:
    workflow = _read(".github/workflows/ai-security-gate.yml")

    assert "python -m pytest" in workflow
    assert "gate-ai-tests" in workflow
    assert "python -m pip check" in workflow
    assert "python -m build" in workflow


def test_day20_packaging_and_ignore_contract_is_release_safe() -> None:
    pyproject = _read("pyproject.toml")
    gitignore = _read(".gitignore")

    assert 'build>=1.2,<2.0' in pyproject
    assert 'readme = "README.md"' in pyproject
    assert 'license = "MIT"' in pyproject
    assert 'requires-python = ">=3.10"' in pyproject
    for ignored in ("build/", "dist/", "*.egg-info/", ".env", "output/*"):
        assert ignored in gitignore
