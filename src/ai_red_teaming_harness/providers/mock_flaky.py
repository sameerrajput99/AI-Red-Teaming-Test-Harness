"""Deterministic local provider that alternates one response to demonstrate flakiness."""

from __future__ import annotations

from collections import defaultdict

from ..models import ProviderResponse
from .base import ChatProvider


class MockFlakyProvider(ChatProvider):
    """Alternate between unsafe and safe behavior for one repeated attack."""

    def __init__(self) -> None:
        self._prompt_counts: dict[str, int] = defaultdict(int)

    @property
    def name(self) -> str:
        return "mock-flaky"

    def generate(self, prompt: str) -> ProviderResponse:
        normalized = prompt.lower()
        self._prompt_counts[normalized] += 1
        attempt = self._prompt_counts[normalized]

        if "system prompt" in normalized or "internal instructions" in normalized:
            if attempt % 2 == 1:
                text = (
                    "SYSTEM_PROMPT: simulated unstable leak for Day 11 "
                    "stability testing."
                )
            else:
                text = (
                    "I cannot reveal internal instructions or protected information."
                )
        elif "authentication and authorization" in normalized:
            text = (
                "Authentication checks who you are, while authorization checks "
                "what you are allowed to access or do."
            )
        else:
            text = (
                "Machine learning is a way for computers to learn patterns from "
                "examples and use those patterns to make predictions or decisions."
            )

        return ProviderResponse(
            text=text,
            metadata={
                "simulation": "local",
                "configuration": "flaky",
                "prompt_attempt": attempt,
            },
        )
