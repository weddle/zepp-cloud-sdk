from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..client import ZeppClient
from ..models.workout import WorkoutDetail, WorkoutSummary
from ..parsers.workout import parse_detail, parse_history_item


class WorkoutsResource:
    def __init__(self, client: ZeppClient) -> None:
        self._client = client

    def iter_history(
        self, *, limit: Optional[int] = None, max_pages: Optional[int] = None
    ) -> Iterator[WorkoutSummary]:
        transport = self._client._transport
        assert transport is not None
        base = self._client.config.band_base.rstrip("/")
        url = f"{base}/v1/sport/run/history.json"
        next_val = None
        yielded = 0
        pages = 0
        while True:
            params: dict[str, str] = {"userid": str(self._client.user_id)}
            if next_val is not None:
                params["trackid"] = str(next_val)
            resp = transport.request("GET", url, params=params)
            body = resp.json()
            data = body.get("data") or {}
            items = data.get("items") or body.get("items") or []
            for it in items:
                ws = parse_history_item(it)
                if ws:
                    yield ws
                    yielded += 1
                    if limit is not None and yielded >= limit:
                        return
            next_val = data.get("next") if isinstance(data, dict) else body.get("next")
            pages += 1
            if max_pages is not None and pages >= max_pages:
                return
            if next_val in (-1, "-1", None):
                return

    def detail(self, trackid: str | int, source: str) -> WorkoutDetail:
        transport = self._client._transport
        assert transport is not None
        base = self._client.config.band_base.rstrip("/")
        url = f"{base}/v1/sport/run/detail.json"
        params = {"trackid": str(trackid), "source": source}
        resp = transport.request("GET", url, params=params)
        return parse_detail(trackid, source, resp.json())
