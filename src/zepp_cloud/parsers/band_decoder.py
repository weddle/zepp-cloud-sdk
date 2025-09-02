from __future__ import annotations

from typing import Any, Optional

from ..models.band import BandDailySummary
from ..utils.base64json import decode_base64_json


def decode_band_summary_item(
    item: dict[str, Any],
    date_hint: Optional[str] = None,
) -> BandDailySummary:
    """Decode and map a single band daily summary item.

    Supports both `summary` and `sum` Base64 fields and retains raw payloads
    for downstream export and debugging.
    """
    # Summary field may be named 'summary' or 'sum'
    b64 = item.get("summary") or item.get("sum")
    if not isinstance(b64, str):
        raise ValueError("band item missing Base64 summary")
    decoded = decode_base64_json(b64)

    stp = decoded.get("stp") or {}
    slp = decoded.get("slp") or {}

    steps_total = int(stp.get("ttl") or 0)
    distance_m = int(stp.get("dis") or 0)
    calories_kcal = int(stp.get("cal") or 0)

    sleep_start_ms = _opt_int(slp.get("st"))
    sleep_end_ms = _opt_int(slp.get("ed"))
    sleep_deep_min = _opt_int(slp.get("dp"))
    sleep_light_min = _opt_int(slp.get("lt"))
    resting_hr = _opt_int(slp.get("rhr"))

    date = (
        item.get("date")
        or item.get("day")
        or (date_hint if isinstance(date_hint, str) else None)
        or ""
    )

    return BandDailySummary(
        date=str(date),
        steps_total=steps_total,
        distance_m=distance_m,
        calories_kcal=calories_kcal,
        sleep_start_ms=sleep_start_ms,
        sleep_end_ms=sleep_end_ms,
        sleep_deep_min=sleep_deep_min,
        sleep_light_min=sleep_light_min,
        resting_hr=resting_hr,
        raw_summary=decoded,
        raw_item=item,
    )


def _opt_int(v: Any) -> Optional[int]:
    try:
        return int(v) if v is not None else None
    except Exception:
        return None
