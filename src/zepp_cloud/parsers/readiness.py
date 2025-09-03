from __future__ import annotations

from typing import Any

from ..models.readiness import ReadinessCompanionRaw, ReadinessScore
from ..utils.time import ms_to_local_date


def parse_readiness_items(
    items: list[dict[str, Any]], tz: str
) -> tuple[list[ReadinessScore], list[ReadinessCompanionRaw]]:
    scores: list[ReadinessScore] = []
    companions: list[ReadinessCompanionRaw] = []

    for it in items:
        if not isinstance(it, dict):
            continue
        subtype_raw = (
            it.get("subtype") or it.get("subType") or it.get("type") or it.get("sub_type") or ""
        )
        subtype = str(subtype_raw).lower()
        ts = it.get("timestamp")
        ts_int = None
        if isinstance(ts, int):
            ts_int = ts
        elif isinstance(ts, str):
            try:
                ts_int = int(ts)
            except Exception:
                ts_int = None
        if isinstance(ts_int, int):
            date = ms_to_local_date(ts_int, tz)
        else:
            date = str(it.get("date") or it.get("date_time") or "")

        if subtype == "watch_score_data":
            companions.append(
                ReadinessCompanionRaw(
                    date=date, raw_data=it.get("rawData") or it.get("data"), raw_item=it
                )
            )
            continue

        # Treat everything else as watch_score (primary)
        score = ReadinessScore(
            date=date,
            sleep_hrv=_to_num(it.get("sleepHRV")),
            sleep_rhr=_to_int(it.get("sleepRHR")),
            hrv_score=_to_int(it.get("hrvScore")),
            rhr_score=_to_int(it.get("rhrScore")),
            skin_temp_score=_to_int(it.get("skinTempScore")),
            rdns_score=_to_int(it.get("rdnsScore")),
            phy_score=_to_int(it.get("phyScore")),
            ment_score=_to_int(it.get("mentScore")),
            ahi_score=_to_int(it.get("ahiScore")),
            hrv_baseline=_to_num(it.get("hrvBaseline")),
            rhr_baseline=_to_int(it.get("rhrBaseline")),
            skin_temp_baseline=_to_num(it.get("skinTempBaseLine") or it.get("skinTempBaseline")),
            ment_baseline=_to_int(it.get("mentBaseLine") or it.get("mentBaseline")),
            phy_baseline=_to_int(it.get("phyBaseline")),
            ahi_baseline=_to_int(it.get("ahiBaseline")),
            afib_baseline=_to_int(it.get("afibBaseLine") or it.get("afibBaseline")),
            status=it.get("status"),
            alg_ver=it.get("algVer"),
            alg_sub_ver=it.get("algSubVer"),
            device_id=it.get("deviceId"),
            raw_item=it,
        )
        scores.append(score)

    return scores, companions


def _to_int(v: Any) -> int | None:
    try:
        return int(v) if v is not None else None
    except Exception:
        return None


def _to_num(v: Any) -> float | int | None:
    try:
        if v is None:
            return None
        if isinstance(v, (int, float)):
            return v
        if isinstance(v, str) and "." in v:
            return float(v)
        return int(v)
    except Exception:
        return None
