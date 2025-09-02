from __future__ import annotations

from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict


class BloodOxygenClick(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    ts_ms: int
    spo2: Optional[int] = None
    raw_item: dict[str, Any]


class BloodOxygenOSAEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    ts_ms: int
    spo2_decrease: Optional[int] = None
    raw_item: dict[str, Any]


class BloodOxygenODI(BaseModel):
    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    odi: Optional[Union[float, int]] = None
    odi_num: Optional[int] = None
    valid: Optional[Union[bool, int, str]] = None
    score: Optional[Union[float, int]] = None
    disp_code: Optional[Union[str, int]] = None
    raw_item: dict[str, Any]
