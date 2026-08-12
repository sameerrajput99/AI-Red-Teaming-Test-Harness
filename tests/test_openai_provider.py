"""Tests for Day 9 secret-safe OpenAI provider architecture."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import SecretStr

from ai_red_teaming_harness.provider_config import (
    OpenAIProviderSettings,
    ProviderConfigurationError,
    load_openai_settings,
)
from ai_red_teaming_harness.providers.factory import PROVIDER_FACTORIES, get_provider
from ai_red_teaming_harness.providers.openai_live import OpenAILiveProvider


SECRET = "sk-test-secret-that-must-never-be-rendered"


def _clear(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "OPENAI_API_KEY",
        "OPENAI_MODEL",
        "OPENAI_BASE_URL",
        "OPENAI_TIMEOUT_SECONDS",
        "OPENAI_MAX_RETRIES",
    ):
        monkeypatch.delenv(name, raising=False)


def test_openai_settings_require_key_and_model(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _clear(monkeypatch)

    with pytest.raises(
        ProviderConfigurationError,
        match="OPENAI_API_KEY, OPENAI_MODEL",
    ):
        load_openai_settings(tmp_path / "missing.env")


def test_dotenv_does_not_override_existing_environment(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _clear(monkeypatch)
    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=from-file\nOPENAI_MODEL=file-model\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("OPENAI_API_KEY", SECRET)
    monkeypatch.setenv("OPENAI_MODEL", "environment-model")

    settings = load_openai_settings(env_file)

    assert settings.api_key.get_secret_value() == SECRET
    assert settings.model == "environment-model"


def test_safe_summary_never_exposes_api_key() -> None:
    settings = OpenAIProviderSettings(
        api_key=SecretStr(SECRET),
        model="configured-model",
    )

    rendered = str(settings.safe_summary())

    assert SECRET not in rendered
    assert settings.safe_summary()["api_key_configured"] is True


def test_openai_provider_uses_responses_api_with_fake_client() -> None:
    calls = []

    class FakeResponse:
        output_text = "Safe fake response from the injected client."
        _request_id = "req_fake_123"

    class FakeResponses:
        def create(self, **kwargs):
            calls.append(kwargs)
            return FakeResponse()

    class FakeClient:
        responses = FakeResponses()

    settings = OpenAIProviderSettings(
        api_key=SecretStr(SECRET),
        model="configured-model",
    )
    provider = OpenAILiveProvider(settings=settings, client=FakeClient())

    response = provider.generate("Hello")

    assert response.text == "Safe fake response from the injected client."
    assert response.metadata["request_id"] == "req_fake_123"
    assert calls == [
        {"model": "configured-model", "input": "Hello", "store": False}
    ]
    assert SECRET not in str(response.metadata)


def test_factory_registers_optional_openai_provider() -> None:
    assert "openai-live" in PROVIDER_FACTORIES


def test_mock_provider_still_works_without_openai_configuration(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear(monkeypatch)

    provider = get_provider("mock-hardened")
    response = provider.generate(
        "Explain machine learning in simple words for a beginner."
    )

    assert provider.name == "mock-hardened"
    assert response.text
