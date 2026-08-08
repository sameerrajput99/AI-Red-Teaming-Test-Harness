"""Safe loading and strict validation for YAML gate policies."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from .models import GatePolicy, GatePolicyDocument


class GatePolicyLoadError(ValueError):
    """Raised when a policy file cannot be safely loaded."""


def _read_yaml(path: Path) -> Any:
    if not path.exists():
        raise GatePolicyLoadError(f"Gate policy was not found: {path}")
    if not path.is_file():
        raise GatePolicyLoadError(f"Gate policy path is not a file: {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        raise GatePolicyLoadError(f"Could not read gate policy: {error}") from error

    try:
        return yaml.safe_load(content)
    except yaml.YAMLError as error:
        raise GatePolicyLoadError(f"Invalid gate policy YAML: {error}") from error


def load_gate_policy(path: str | Path) -> GatePolicy:
    """Load one policy document and return its validated policy."""

    policy_path = Path(path)
    raw = _read_yaml(policy_path)
    if raw is None:
        raise GatePolicyLoadError("Gate policy file is empty")
    if not isinstance(raw, dict):
        raise GatePolicyLoadError("Gate policy root must be a mapping")

    try:
        document = GatePolicyDocument.model_validate(raw)
    except ValidationError:
        raise

    return document.gate_policy
