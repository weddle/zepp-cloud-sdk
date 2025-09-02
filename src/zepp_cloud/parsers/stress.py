from __future__ import annotations

import json
from typing import Any

from ..models.stress import StressDay, StressPoint
from ..utils.time import ms_to_local_date


def parse_stress_item(item: dict[str, Any], tz: str) -> StressDay:
    data_str = item.get("data")
    pts: list[StressPoint] = []
    if isinstance(data_str, str) and data_str:
        try:
            arr = json.loads(data_str)
            if isinstance(arr, list):
                for e in arr:
                    if not isinstance(e, dict):
                        continue
                    t = e.get("time")
                    v = e.get("value")
                    try:
                        if t is None or v is None:
                            continue
                        pts.append(StressPoint(time_ms=int(t), value=int(v)))
                    except Exception:
                        continue
        except Exception:
            pass

    # Determine local date using top-level timestamp if available, else first point
    ts = item.get("timestamp")
    if not isinstance(ts, int) and pts:
        ts = pts[0].time_ms
    date = ms_to_local_date(int(ts), tz) if isinstance(ts, int) else ""

    # Stats: prefer top-level minStress/maxStress if provided
    min_v = item.get("minStress")
    max_v = item.get("maxStress")
    avg_v = None
    if min_v is None or max_v is None:
        if pts:
            values = [p.value for p in pts]
            min_v = min_v if min_v is not None else min(values)
            max_v = max_v if max_v is not None else max(values)
            avg_v = sum(values) / len(values)
    elif pts:
        values = [p.value for p in pts]
        avg_v = sum(values) / len(values)

    return StressDay(
        date=str(date),
        points=pts,
        min=int(min_v) if min_v is not None else None,
        max=int(max_v) if max_v is not None else None,
        avg=float(avg_v) if avg_v is not None else None,
        raw_item=item,
    )
