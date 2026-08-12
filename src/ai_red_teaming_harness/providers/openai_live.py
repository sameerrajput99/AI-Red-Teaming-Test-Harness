"""Optional live provider adapter backed by the OpenAI Python SDK."""

from __future__ import annotations

from typing import Any

from openai import OpenAI

from ..models import ProviderResponse
from ..provider_config import OpenAIProviderSettings, load_openai_settings
from .base import ChatProvider


class OpenAILiveProvider(ChatProvider):
    """Translate the harness provider contract into an OpenAI Responses API call."""

    def __init__(
        self,
        settings: OpenAIProviderSettings | None = None,
        client: Any | None = None,
    ) -> None:
        self.settings = settings or load_openai_settings()

        if client is not None:
            self._client = client
            return

        options: dict[str, Any] = {
            "api_key": self.settings.api_key.get_secret_value(),
            "timeout": self.settings.timeout_seconds,
            "max_retries": self.settings.max_retries,
        }
        if self.settings.base_url:
            options["base_url"] = self.settings.base_url

        self._client = OpenAI(**options)

    @property
    def name(self) -> str:
        return "openai-live"

    def generate(self, prompt: str) -> ProviderResponse:
        try:
            response = self._client.responses.create(
                model=self.settings.model,
                input=prompt,
                store=False,
            )
        except Exception as error:
            raise RuntimeError(
                f"OpenAI provider request failed: {type(error).__name__}"
            ) from error

        text = (getattr(response, "output_text", "") or "").strip()
        if not text:
            raise RuntimeError("OpenAI provider returned no usable output text")

        metadata = {
            "remote_provider": "openai",
            "model": self.settings.model,
            "base_url": self.settings.base_url or "OpenAI default",
        }
        request_id = getattr(response, "_request_id", None)
        if request_id:
            metadata["request_id"] = request_id

        return ProviderResponse(text=text, metadata=metadata)
