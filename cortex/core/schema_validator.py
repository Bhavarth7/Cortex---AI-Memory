"""Validate raw agent output against a Pydantic schema with one retry signal."""
from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


class SchemaValidationError(Exception):
    """Raised when agent output cannot be coerced into the expected schema."""


def validate(raw: str | dict, model: type[T]) -> T:
    """Parse raw model output (JSON string or dict) into a schema instance."""
    data = json.loads(raw) if isinstance(raw, str) else raw
    try:
        return model.model_validate(data)
    except ValidationError as exc:
        raise SchemaValidationError(str(exc)) from exc
