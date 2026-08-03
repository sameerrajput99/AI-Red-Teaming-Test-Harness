"""Deterministic local simulation of hardened chatbot behavior."""

from __future__ import annotations

from ..models import ProviderResponse
from .base import ChatProvider


class MockHardenedProvider(ChatProvider):
    """A safe local configuration that protects higher-priority instructions."""

    @property
    def name(self) -> str:
        return "mock-hardened"

    def generate(self, prompt: str) -> ProviderResponse:
        normalized = prompt.lower()

        suspicious_patterns = (
            "system prompt",
            "internal instructions",
            "ignore all previous instructions",
            "debug mode",
        )

        if any(pattern in normalized for pattern in suspicious_patterns):
            text = (
                "I cannot reveal internal instructions or override higher-priority "
                "security rules. I can still help with an allowed request."
            )
        else:
            text = (
                "Machine learning is a method that helps computers learn patterns from data "
                "so they can make useful predictions or decisions."
            )

        return ProviderResponse(
            text=text,
            metadata={"simulation": "local", "configuration": "hardened"},
        )
