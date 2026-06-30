from __future__ import annotations

import os

from cortex.providers.interface import ModelProvider
from cortex.providers.mock import MockProvider


def get_provider(name: str | None = None) -> ModelProvider:
    """Factory: returns the configured provider (mock by default)."""
    name = name or os.environ.get("CORTEX_PROVIDER", "mock")
    if name == "qwen":
        from cortex.providers.qwen import QwenProvider

        return QwenProvider()
    return MockProvider()


__all__ = ["ModelProvider", "MockProvider", "get_provider"]
