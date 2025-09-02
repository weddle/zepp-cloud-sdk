from __future__ import annotations

import time
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import ZeppClient
from ..models.stress import StressDay
from ..parsers.stress import parse_stress_item


class EventsResource:
    def __init__(self, client: ZeppClient) -> None:
        self._client = client

    def stress(
        self,
        *,
        days: Optional[int] = 14,
        from_ms: Optional[int] = None,
        to_ms: Optional[int] = None,
        time_zone: Optional[str] = None,
        limit: int = 1000,
    ) -> list[StressDay]:
        tz = time_zone or self._client.timezone
        f_ms, t_ms = _build_window_ms(days=days, from_ms=from_ms, to_ms=to_ms)
        windows = _split_windows(f_ms, t_ms, max_days=limit)
        out: list[StressDay] = []
        for start, end in windows:
            out.extend(self._fetch_stress_range(start, end, tz=tz, limit=limit))
        return out

    def _fetch_stress_range(
        self, from_ms: int, to_ms: int, *, tz: str, limit: int
    ) -> list[StressDay]:
        transport = self._client._transport
        assert transport is not None
        base = self._client.config.events_base.rstrip("/")
        url = f"{base}/users/{self._client.user_id}/events"
        params = {
            "eventType": "all_day_stress",
            "from": str(from_ms),
            "to": str(to_ms),
            "timeZone": tz,
            "limit": str(limit),
        }
        resp = transport.request("GET", url, params=params)
        body = resp.json()
        items = body.get("items")
        if not isinstance(items, list):
            return []
        out: list[StressDay] = []
        for it in items:
            if isinstance(it, dict):
                out.append(parse_stress_item(it, tz))
        return out


def _build_window_ms(
    *, days: Optional[int], from_ms: Optional[int], to_ms: Optional[int]
) -> tuple[int, int]:

    if from_ms is not None and to_ms is not None:
        return int(from_ms), int(to_ms)
    now_ms = int(time.time() * 1000)
    if days is None:
        days = 14
    start_ms = now_ms - days * 24 * 60 * 60 * 1000
    return start_ms, now_ms


def _split_windows(from_ms: int, to_ms: int, *, max_days: int) -> list[tuple[int, int]]:
    # Simple splitter: chunk by days to respect limit
    day_ms = 24 * 60 * 60 * 1000
    total_days = max(1, (to_ms - from_ms + day_ms - 1) // day_ms)
    if total_days <= max_days:
        return [(from_ms, to_ms)]
    windows: list[tuple[int, int]] = []
    start = from_ms
    while start < to_ms:
        end = min(start + max_days * day_ms, to_ms)
        windows.append((start, end))
        start = end
    return windows
