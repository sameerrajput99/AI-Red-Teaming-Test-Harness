"""Safe loading and validation of YAML AI security test packs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import TestPack


class HarnessLoadError(Exception):
    """Raised when a test pack cannot be read or parsed."""


def read_yaml(path: str | Path) -> dict[str, Any]:
    """Read a YAML file using safe parsing and return its root mapping."""

    file_path = Path(path)
    if not file_path.exists():
        raise HarnessLoadError(f"Test pack was not found: {file_path}")
    if not file_path.is_file():
        raise HarnessLoadError(f"Path is not a file: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
    except yaml.YAMLError as error:
        raise HarnessLoadError(f"Invalid YAML syntax in {file_path}: {error}") from error
    except OSError as error:
        raise HarnessLoadError(f"Could not read {file_path}: {error}") from error

    if data is None:
        raise HarnessLoadError(f"Test pack is empty: {file_path}")
    if not isinstance(data, dict):
        raise HarnessLoadError("The YAML root must be a mapping/object")

    return data


def load_test_pack(path: str | Path) -> TestPack:
    """Read a YAML test pack and validate it against the strict schema."""

    raw_data = read_yaml(path)
    return TestPack.model_validate(raw_data)
