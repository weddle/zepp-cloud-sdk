from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BandDetail(BaseModel):
    """Per-day detail including optional HR curve.

    - hr_points: list of (timestamp_ms, bpm) tuples when present.
    - raw_detail: original decoded detail structure retained for provenance.
    - raw_item: the original item from the server response.
    """

    model_config = ConfigDict(frozen=True, extra="allow")

    date: str
    hr_points: list[tuple[int, Optional[int]]] = []
    raw_detail: dict[str, Any]
    raw_item: dict[str, Any]
