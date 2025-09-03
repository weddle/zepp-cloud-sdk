from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict


class WorkoutSummary(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    trackid: Union[str, int]
    source: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    duration_s: Optional[int] = None
    distance_m: Optional[int] = None
    calories_kcal: Optional[int] = None
    sport_mode: Optional[Union[str, int]] = None
    raw_item: dict[str, Any]


class WorkoutDetail(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    trackid: Union[str, int]
    source: str
    summary: WorkoutSummary
    series: Optional[dict[str, Any]] = None
    track: Optional[list[Any]] = None
    raw_detail: dict[str, Any]

