"""Model provider abstraction. All agent calls go through this."""
from __future__ import annotations

from abc import ABC, abstractmethod


class ModelProvider(ABC):
    @abstractmethod
    def generate(
        self,
        messages: list[dict],
        model: str,
        temperature: float = 0.7,
        schema: dict | None = None,
    ) -> str:
        """Return the model's text/JSON response."""

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """Return an embedding vector for the given text."""
