"""Provider selection for command-line workflows."""

from __future__ import annotations

from .base import ChatProvider
from .mock_flaky import MockFlakyProvider
from .mock_hardened import MockHardenedProvider
from .mock_vulnerable import MockVulnerableProvider
from .openai_live import OpenAILiveProvider


PROVIDER_FACTORIES = {
    "mock-vulnerable": MockVulnerableProvider,
    "mock-hardened": MockHardenedProvider,
    "mock-flaky": MockFlakyProvider,
    "openai-live": OpenAILiveProvider,
}


def get_provider(name: str) -> ChatProvider:
    normalized = name.strip().lower()
    factory = PROVIDER_FACTORIES.get(normalized)
    if factory is None:
        supported = ", ".join(sorted(PROVIDER_FACTORIES))
        raise ValueError(
            f"Unknown provider '{name}'. Supported providers: {supported}"
        )
    return factory()
