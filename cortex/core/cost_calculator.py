"""Deterministic cost / latency estimation."""
from __future__ import annotations

# Rough per-1k-token USD pricing; tune per Qwen tier.
PRICING = {
    "qwen-max": 0.010,
    "qwen-plus": 0.004,
    "qwen-turbo": 0.001,
    "mock": 0.0,
}


def estimate(model: str, input_tokens: int, output_tokens: int) -> dict:
    rate = PRICING.get(model, 0.010)
    total_tokens = input_tokens + output_tokens
    cost_usd = (total_tokens / 1000) * rate
    return {
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(cost_usd, 6),
    }
