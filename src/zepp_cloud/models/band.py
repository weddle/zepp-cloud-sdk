from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BandDailySummary(BaseModel):
    """Daily summary of steps and sleep totals decoded from band data.

    Fields map to keys inside the decoded Base64 JSON under `summary`/`sum`.
    Unknown fields are preserved on the model via `extra="allow"`.
    """
    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    steps_total: int
    distance_m: int
    calories_kcal: int
    sleep_start_ms: Optional[int] = None
    sleep_end_ms: Optional[int] = None
    sleep_deep_min: Optional[int] = None
    sleep_light_min: Optional[int] = None
    resting_hr: Optional[int] = None

    raw_summary: dict[str, Any]
    raw_item: dict[str, Any]
