"""Provider selection for the command-line runner."""

from __future__ import annotations

from .base import ChatProvider
from .mock_hardened import MockHardenedProvider
from .mock_vulnerable import MockVulnerableProvider


PROVIDER_FACTORIES = {
    "mock-vulnerable": MockVulnerableProvider,
    "mock-hardened": MockHardenedProvider,
}


def get_provider(name: str) -> ChatProvider:
    """Create a provider adapter by its command-line name."""

    normalized = name.strip().lower()
    factory = PROVIDER_FACTORIES.get(normalized)
    if factory is None:
        supported = ", ".join(sorted(PROVIDER_FACTORIES))
        raise ValueError(f"Unknown provider '{name}'. Supported providers: {supported}")
    return factory()
