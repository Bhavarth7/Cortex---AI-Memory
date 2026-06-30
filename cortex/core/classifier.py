"""Deterministic keyword-based task tag classifier.

Maps free-text task descriptions onto the controlled tag vocabulary
(see config/tags.json). Cheap, explainable, and provider-free. A real
deployment can swap this for a model call that emits the same vocabulary.
"""
from __future__ import annotations

KEYWORDS: dict[str, list[str]] = {
    "rag": ["rag", "retrieval", "vector", "embedding", "knowledge base"],
    "regulated_domain": [
        "health", "healthcare", "patient", "hipaa", "medical",
        "insurance", "claims", "compliance", "finance", "financial",
        "bank", "legal", "gdpr", "regulated",
    ],
    "real_time_system": ["real-time", "real time", "streaming", "live"],
    "multimodal": ["image", "audio", "video", "multimodal", "vision", "speech"],
    "cost_sensitive": ["cheap", "budget", "cost-sensitive", "low cost", "low-cost"],
    "latency_sensitive": ["latency", "fast", "low-latency", "responsive"],
    "agentic_workflow": ["agent", "agentic", "workflow", "orchestration", "tool use"],
    "customer_support": ["support", "helpdesk", "ticket", "customer service"],
    "document_ai": ["document", "pdf", "ocr", "extraction", "invoice"],
    "security_sensitive": ["security", "auth", "encryption", "secure", "access control"],
}


def classify_tags(text: str, extra: list[str] | None = None) -> list[str]:
    """Return the sorted set of vocabulary tags that match the text."""
    lowered = text.lower()
    tags = set(extra or [])
    for tag, kws in KEYWORDS.items():
        if any(kw in lowered for kw in kws):
            tags.add(tag)
    return sorted(tags)
