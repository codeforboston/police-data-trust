from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

from deepdiff import DeepDiff


def _normalize_for_diff(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _normalize_for_diff(val)
            for key, val in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_normalize_for_diff(item) for item in value]
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    return value


def make_citation_diff(old: dict[str, Any], new: dict[str, Any]) -> str | None:
    diff = DeepDiff(
        _normalize_for_diff(old),
        _normalize_for_diff(new),
        ignore_order=True,
    )
    if not diff:
        return None
    return diff.to_json()
