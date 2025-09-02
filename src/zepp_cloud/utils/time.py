from __future__ import annotations

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def local_midnight_epoch_ms(date_str: str, tz_name: str) -> int:
    """Return epoch ms for local midnight of date_str in tz_name.

    date_str: YYYY-MM-DD
    tz_name: IANA timezone, e.g., "America/New_York"
    """
    try:
        y, m, d = map(int, date_str.split("-"))
        tz = ZoneInfo(tz_name)
    except Exception:
        y, m, d = map(int, date_str.split("-"))
        tz = timezone.utc
    dt_local = datetime(y, m, d, 0, 0, 0, tzinfo=tz)
    dt_utc = dt_local.astimezone(timezone.utc)
    return int(dt_utc.timestamp() * 1000)


def ms_to_local_date(ms: int, tz_name: str) -> str:
    tz = None
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = timezone.utc
    dt = datetime.fromtimestamp(ms / 1000.0, tz=timezone.utc).astimezone(tz)
    return dt.strftime("%Y-%m-%d")
