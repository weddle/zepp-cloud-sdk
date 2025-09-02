from __future__ import annotations

import base64
from contextlib import suppress
from typing import Any

from ..models.band_detail import BandDetail
from ..utils.base64json import decode_base64_json
from ..utils.time import local_midnight_epoch_ms


def decode_band_detail_item(
    item: dict[str, Any],
    date_hint: str | None = None,
    timezone: str | None = None,
    keep_invalid: bool = False,
) -> BandDetail:
    """Decode a band detail item into BandDetail.

    Attempts to extract an HR curve from commonly observed shapes:
    - detail.hr as list[[ts, value], ...]
    - detail.hr as list[{"time": ts, "value": v}] or {"ts": ts, "bpm": v}
    Unrecognized series are preserved in raw_detail.
    """
    detail = item.get("detail") or {}
    hr_points: list[tuple[int, int]] = []

    hr = None
    if isinstance(detail, dict):
        # prefer 'hr' key if present
        hr = detail.get("hr") or detail.get("hr_points") or detail.get("hrSeries")

    if isinstance(hr, list):
        for elem in hr:
            # Pair form [ts, value]
            if isinstance(elem, list) and len(elem) >= 2:
                try:
                    ts = int(elem[0])
                    val = int(elem[1])
                    hr_points.append((ts, val))
                except Exception:
                    continue
            # Dict form
            elif isinstance(elem, dict):
                ts_like = elem.get("time") or elem.get("ts") or elem.get("timestamp")
                v_like = elem.get("value") or elem.get("bpm") or elem.get("hr")
                try:
                    if ts_like is not None and v_like is not None:
                        hr_points.append((int(ts_like), int(v_like)))
                except Exception:
                    continue

    # Derive date; detail payloads sometimes use 'date_time'
    date = item.get("date") or item.get("day") or item.get("date_time") or date_hint or ""
    # Build a richer raw_detail when 'detail' is not present
    raw_detail: dict[str, Any] = {}
    if isinstance(detail, dict) and detail:
        raw_detail.update(detail)
    # Include decoded summary if available to aid analysis
    b64_summary = item.get("summary")
    if isinstance(b64_summary, str):
        with suppress(Exception):
            raw_detail["summary"] = decode_base64_json(b64_summary)
    # Note presence/length of data and data_hr blobs (device-dependent)
    for key in ("data", "data_hr"):
        val = item.get(key)
        if isinstance(val, str):
            try:
                raw = base64.b64decode(val)
                raw_detail[f"{key}_bytes_len"] = len(raw)
                raw_detail[f"{key}_present"] = True
            except Exception:
                raw_detail[f"{key}_present"] = True

    # If no JSON hr curve, attempt to decode data_hr per BTasker docs
    if not hr_points:
        b64_hr = item.get("data_hr")
        if isinstance(b64_hr, str) and date:
            with suppress(Exception):
                raw = base64.b64decode(b64_hr)
                base_ms = local_midnight_epoch_ms(str(date), timezone or "UTC")
                out: list[tuple[int, int]] = []
                for i, b in enumerate(raw):
                    # 254/255 indicate invalid/no read; 0 also considered invalid
                    ts = base_ms + i * 60_000
                    if b in (254, 255, 0):
                        if keep_invalid:
                            out.append((ts, None))
                    else:
                        out.append((ts, int(b)))
                hr_points = out

    return BandDetail(date=str(date), hr_points=hr_points, raw_detail=raw_detail, raw_item=item)
