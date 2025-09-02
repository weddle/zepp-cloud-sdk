from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class StressPoint(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    time_ms: int
    value: int


class StressDay(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    points: list[StressPoint]
    min: Optional[int] = None
    max: Optional[int] = None
    avg: Optional[float] = None
    raw_item: dict[str, Any]

