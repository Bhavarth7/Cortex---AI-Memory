"""Qwen / Alibaba Cloud provider (OpenAI-compatible endpoint).

Primary provider for production. Uses the DashScope compatible-mode API.
"""
from __future__ import annotations

import json
import os

import httpx

from cortex.providers.interface import ModelProvider


class QwenProvider(ModelProvider):
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        embed_model: str | None = None,
    ) -> None:
        self.api_key = api_key or os.environ["QWEN_API_KEY"]
        self.base_url = base_url or os.environ.get(
            "QWEN_BASE_URL",
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        self.model = model or os.environ.get("QWEN_MODEL", "qwen-max")
        self.embed_model = embed_model or os.environ.get(
            "QWEN_EMBED_MODEL", "text-embedding-v3"
        )

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        messages: list[dict],
        model: str | None = None,
        temperature: float = 0.7,
        schema: dict | None = None,
    ) -> str:
        body: dict = {
            "model": model or self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if schema is not None:
            body["response_format"] = {"type": "json_object"}
        resp = httpx.post(
            f"{self.base_url}/chat/completions",
            headers=self._headers(),
            json=body,
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]

    def embed(self, text: str) -> list[float]:
        resp = httpx.post(
            f"{self.base_url}/embeddings",
            headers=self._headers(),
            json={"model": self.embed_model, "input": text},
            timeout=60.0,
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]
