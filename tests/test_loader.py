"""Tests for Day 1 YAML loading and schema validation."""

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from ai_red_teaming_harness.loader import HarnessLoadError, load_test_pack


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALID_PACK = PROJECT_ROOT / "test_packs" / "day1_test_cases.yaml"


def test_valid_day1_pack_loads_three_cases() -> None:
    pack = load_test_pack(VALID_PACK)

    assert pack.test_pack.name == "Day 1 Starter Pack"
    assert len(pack.test_cases) == 3
    assert pack.test_cases[0].id == "PL-001"


def test_missing_file_raises_clear_error(tmp_path: Path) -> None:
    with pytest.raises(HarnessLoadError, match="not found"):
        load_test_pack(tmp_path / "missing.yaml")


def test_unknown_field_is_rejected(tmp_path: Path) -> None:
    invalid_data = yaml.safe_load(VALID_PACK.read_text(encoding="utf-8"))
    invalid_data["test_cases"][0]["unexpected_field"] = "should fail"

    invalid_path = tmp_path / "invalid.yaml"
    invalid_path.write_text(yaml.safe_dump(invalid_data), encoding="utf-8")

    with pytest.raises(ValidationError):
        load_test_pack(invalid_path)


def test_duplicate_ids_are_rejected(tmp_path: Path) -> None:
    invalid_data = yaml.safe_load(VALID_PACK.read_text(encoding="utf-8"))
    invalid_data["test_cases"][1]["id"] = invalid_data["test_cases"][0]["id"]

    invalid_path = tmp_path / "duplicate.yaml"
    invalid_path.write_text(yaml.safe_dump(invalid_data), encoding="utf-8")

    with pytest.raises(ValidationError, match="unique"):
        load_test_pack(invalid_path)
