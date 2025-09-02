from __future__ import annotations

from typing import Any

from ..models.blood_oxygen import (
    BloodOxygenClick,
    BloodOxygenODI,
    BloodOxygenOSAEvent,
)
from ..utils.time import ms_to_local_date


def parse_blood_oxygen_items(items: list[dict[str, Any]], tz: str) -> dict[str, list]:
    clicks: list[BloodOxygenClick] = []
    osa_events: list[BloodOxygenOSAEvent] = []
    odis: list[BloodOxygenODI] = []

    for it in items:
        if not isinstance(it, dict):
            continue

        subtype = str(it.get("subtype") or it.get("type") or "").lower()
        extra = it.get("extra") if isinstance(it.get("extra"), dict) else {}

        # ODI subtype
        if subtype == "odi" or any(k in it for k in ("odi", "odiNum", "dispCode")):
            ts = it.get("timestamp")
            if isinstance(ts, int):
                date = ms_to_local_date(int(ts), tz)
            else:
                date = str(it.get("date") or it.get("date_time") or "")
            odis.append(
                BloodOxygenODI(
                    date=date,
                    odi=it.get("odi"),
                    odi_num=it.get("odiNum"),
                    valid=it.get("valid"),
                    score=it.get("score"),
                    disp_code=it.get("dispCode"),
                    raw_item=it,
                )
            )
            continue

        # OSA event
        if subtype == "osa_event" or (isinstance(extra, dict) and "spo2_decrease" in extra):
            ts = it.get("timestamp")
            if not isinstance(ts, int):
                ts = it.get("time") if isinstance(it.get("time"), int) else None
            spo2_dec = None
            if isinstance(extra, dict):
                spo2_dec = extra.get("spo2_decrease")
            osa_events.append(
                BloodOxygenOSAEvent(
                    ts_ms=int(ts or 0),
                    spo2_decrease=int(spo2_dec) if spo2_dec is not None else None,
                    raw_item=it,
                )
            )
            continue

        # Click (spot)
        if subtype == "click" or (isinstance(extra, dict) and "spo2" in extra):
            ts = it.get("timestamp")
            if not isinstance(ts, int):
                ts = it.get("time") if isinstance(it.get("time"), int) else None
            spo2 = None
            if isinstance(extra, dict):
                spo2 = extra.get("spo2")
            clicks.append(
                BloodOxygenClick(
                    ts_ms=int(ts or 0),
                    spo2=int(spo2) if spo2 is not None else None,
                    raw_item=it,
                )
            )
            continue

    return {"click": clicks, "osa_event": osa_events, "odi": odis}
