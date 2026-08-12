"""Secret-safe configuration loading for optional remote providers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator


class ProviderConfigurationError(ValueError):
    """Raised when a selected remote provider is not safely configured."""


class OpenAIProviderSettings(BaseModel):
    """Validated OpenAI provider settings with a secret-safe API key."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    api_key: SecretStr
    model: str = Field(min_length=1, max_length=200)
    base_url: str | None = Field(default=None, max_length=500)
    timeout_seconds: float = Field(default=30.0, gt=0, le=300)
    max_retries: int = Field(default=2, ge=0, le=10)

    @field_validator("model")
    @classmethod
    def reject_placeholder_model(cls, value: str) -> str:
        normalized = value.strip()
        if normalized.lower().startswith("replace-with"):
            raise ValueError("OPENAI_MODEL still contains the example placeholder")
        return normalized

    @field_validator("base_url")
    @classmethod
    def normalize_base_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            return None
        if not normalized.startswith(("https://", "http://")):
            raise ValueError("OPENAI_BASE_URL must start with http:// or https://")
        return normalized.rstrip("/")

    def safe_summary(self) -> dict[str, Any]:
        return {
            "provider": "openai-live",
            "api_key_configured": bool(self.api_key.get_secret_value()),
            "model": self.model,
            "base_url": self.base_url or "OpenAI default",
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
        }


def _load_environment(env_file: str | Path | None = ".env") -> None:
    if env_file is not None:
        load_dotenv(dotenv_path=Path(env_file), override=False)


def _parse_float(name: str, raw: str | None, default: float) -> float:
    if raw is None or not raw.strip():
        return default
    try:
        return float(raw)
    except ValueError as error:
        raise ProviderConfigurationError(f"{name} must be a number") from error


def _parse_int(name: str, raw: str | None, default: int) -> int:
    if raw is None or not raw.strip():
        return default
    try:
        return int(raw)
    except ValueError as error:
        raise ProviderConfigurationError(f"{name} must be an integer") from error


def inspect_openai_environment(env_file: str | Path | None = ".env") -> dict[str, Any]:
    _load_environment(env_file)
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    model = (os.getenv("OPENAI_MODEL") or "").strip()
    base_url = (os.getenv("OPENAI_BASE_URL") or "").strip()
    return {
        "provider": "openai-live",
        "api_key_configured": bool(api_key and not api_key.lower().startswith("replace-with")),
        "model": model if model and not model.lower().startswith("replace-with") else "<missing>",
        "base_url": base_url or "OpenAI default",
        "timeout_seconds": os.getenv("OPENAI_TIMEOUT_SECONDS", "30"),
        "max_retries": os.getenv("OPENAI_MAX_RETRIES", "2"),
    }


def load_openai_settings(env_file: str | Path | None = ".env") -> OpenAIProviderSettings:
    _load_environment(env_file)
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    model = (os.getenv("OPENAI_MODEL") or "").strip()

    missing = []
    if not api_key or api_key.lower().startswith("replace-with"):
        missing.append("OPENAI_API_KEY")
    if not model or model.lower().startswith("replace-with"):
        missing.append("OPENAI_MODEL")
    if missing:
        raise ProviderConfigurationError(
            f"Missing required environment variable(s): {', '.join(missing)}"
        )

    try:
        return OpenAIProviderSettings(
            api_key=SecretStr(api_key),
            model=model,
            base_url=os.getenv("OPENAI_BASE_URL"),
            timeout_seconds=_parse_float(
                "OPENAI_TIMEOUT_SECONDS", os.getenv("OPENAI_TIMEOUT_SECONDS"), 30.0
            ),
            max_retries=_parse_int(
                "OPENAI_MAX_RETRIES", os.getenv("OPENAI_MAX_RETRIES"), 2
            ),
        )
    except ValueError as error:
        raise ProviderConfigurationError(
            f"Invalid openai-live configuration: {error}"
        ) from error
