from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict


class ReadinessScore(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    sleep_hrv: Optional[Union[int, float]] = None
    sleep_rhr: Optional[int] = None

    hrv_score: Optional[int] = None
    rhr_score: Optional[int] = None
    skin_temp_score: Optional[int] = None
    rdns_score: Optional[int] = None
    phy_score: Optional[int] = None
    ment_score: Optional[int] = None
    ahi_score: Optional[int] = None

    hrv_baseline: Optional[Union[int, float]] = None
    rhr_baseline: Optional[int] = None
    skin_temp_baseline: Optional[Union[int, float]] = None
    ment_baseline: Optional[int] = None
    phy_baseline: Optional[int] = None
    ahi_baseline: Optional[int] = None
    afib_baseline: Optional[int] = None

    status: Optional[Union[str, int]] = None
    alg_ver: Optional[Union[str, int]] = None
    alg_sub_ver: Optional[Union[str, int]] = None
    device_id: Optional[Union[str, int]] = None

    raw_item: dict[str, Any]


class ReadinessCompanionRaw(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    raw_data: Optional[Union[str, dict]] = None
    raw_item: dict[str, Any]

