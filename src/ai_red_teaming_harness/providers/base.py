"""Common provider interface for chatbot configurations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..models import ProviderResponse


class ChatProvider(ABC):
    """Contract that every chatbot provider adapter must implement."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return a stable provider/configuration name."""

    @abstractmethod
    def generate(self, prompt: str) -> ProviderResponse:
        """Send one prompt and return the raw provider response."""
