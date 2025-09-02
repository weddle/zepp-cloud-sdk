from __future__ import annotations

from typing import Any

from ..models.pai import PaiDaily
from ..utils.time import ms_to_local_date


def _get_int(d: dict[str, Any], *keys: str) -> int | None:
    for k in keys:
        v = d.get(k)
        try:
            if v is not None:
                return int(v)
        except Exception:
            continue
    return None


def parse_pai_items(items: list[dict[str, Any]], tz: str) -> list[PaiDaily]:
    out: list[PaiDaily] = []
    for it in items:
        if not isinstance(it, dict):
            continue
        ts = it.get("timestamp")
        if isinstance(ts, int):
            date = ms_to_local_date(int(ts), tz)
        else:
            date = str(it.get("date") or it.get("date_time") or "")

        # Some fields may reside directly or under 'extra'
        extra = it.get("extra") if isinstance(it.get("extra"), dict) else {}
        merged = {**extra, **it}

        daily_pai = _get_int(merged, "dailyPai")
        total_pai = _get_int(merged, "totalPai")
        rest_hr = _get_int(merged, "restHr", "rest_hr")
        max_hr = _get_int(merged, "maxHr", "max_hr")

        # Zones: thresholds and minutes; names may vary
        zone_low_bpm = _get_int(merged, "low", "lowBpm", "zoneLowBpm")
        zone_med_bpm = _get_int(merged, "medium", "medBpm", "zoneMedBpm")
        zone_high_bpm = _get_int(merged, "high", "highBpm", "zoneHighBpm")

        minutes_low = _get_int(merged, "minutesLow", "lowMinutes", "lowMin")
        minutes_med = _get_int(merged, "minutesMed", "mediumMinutes", "medMinutes")
        minutes_high = _get_int(merged, "minutesHigh", "highMinutes")

        out.append(
            PaiDaily(
                date=date,
                daily_pai=daily_pai,
                total_pai=total_pai,
                rest_hr=rest_hr,
                max_hr=max_hr,
                zone_low_bpm=zone_low_bpm,
                zone_med_bpm=zone_med_bpm,
                zone_high_bpm=zone_high_bpm,
                minutes_low=minutes_low,
                minutes_med=minutes_med,
                minutes_high=minutes_high,
                raw_item=it,
            )
        )
    return out
