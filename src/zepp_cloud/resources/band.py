from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ..models.band import BandDailySummary
from ..models.band_detail import BandDetail
from ..parsers.band_decoder import decode_band_summary_item
from ..parsers.band_detail import decode_band_detail_item

if TYPE_CHECKING:
    from ..client import ZeppClient


class BandResource:
    def __init__(self, client: ZeppClient) -> None:
        self._client = client

    def get_summary(self, from_date: str, to_date: str) -> list[BandDailySummary]:
        """Fetch daily band summaries for the given date range.

        - Dates are `YYYY-MM-DD` and typically inclusive on both ends per server behavior.
        - Returns parsed `BandDailySummary` items with raw payloads retained.
        """
        transport = self._client._transport
        assert transport is not None, "Client transport not initialized"

        url = f"{self._client.config.band_base}/v1/data/band_data.json"
        params = {
            "query_type": "summary",
            "device_type": "android_phone",
            "userid": self._client.user_id,
            "from_date": from_date,
            "to_date": to_date,
        }
        resp = transport.request("GET", url, params=params)
        data = resp.json()
        items = _coerce_items(data.get("data"))

        out: list[BandDailySummary] = []
        for item in items:
            # If items came from dict keyed by date, pass its key as hint.
            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
                k, v = item
                out.append(decode_band_summary_item(v, date_hint=k))
            elif isinstance(item, dict):
                out.append(decode_band_summary_item(item))
        return out

    def get_detail(
        self, from_date: str, to_date: str, *, keep_invalid: bool = False
    ) -> list[BandDetail]:
        """Fetch band detail windows for the given date range.

        Attempts to normalize HR curve series when present, and keeps the
        original detail structure in `raw_detail`.
        """
        transport = self._client._transport
        assert transport is not None, "Client transport not initialized"

        url = f"{self._client.config.band_base}/v1/data/band_data.json"
        params = {
            "query_type": "detail",
            "device_type": "android_phone",
            "userid": self._client.user_id,
            "from_date": from_date,
            "to_date": to_date,
        }
        resp = transport.request("GET", url, params=params)
        data = resp.json()
        items = _coerce_items(data.get("data"))

        out: list[BandDetail] = []
        for item in items:
            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], str):
                k, v = item
                if isinstance(v, dict):
                    out.append(
                        decode_band_detail_item(
                            v,
                            date_hint=k,
                            timezone=self._client.timezone,
                            keep_invalid=keep_invalid,
                        )
                    )
            elif isinstance(item, dict):
                out.append(
                    decode_band_detail_item(
                        item, timezone=self._client.timezone, keep_invalid=keep_invalid
                    )
                )
        return out


def _coerce_items(data_field: Any) -> Iterable[Any]:
    if data_field is None:
        return []
    if isinstance(data_field, list):
        return data_field
    if isinstance(data_field, dict):
        # Yield pairs so we can retain the date key as a hint
        return list(data_field.items())
    return []
