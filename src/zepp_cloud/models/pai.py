from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class PaiDaily(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    daily_pai: Optional[int] = None
    total_pai: Optional[int] = None
    rest_hr: Optional[int] = None
    max_hr: Optional[int] = None

    zone_low_bpm: Optional[int] = None
    zone_med_bpm: Optional[int] = None
    zone_high_bpm: Optional[int] = None

    minutes_low: Optional[int] = None
    minutes_med: Optional[int] = None
    minutes_high: Optional[int] = None

    raw_item: dict[str, Any]
