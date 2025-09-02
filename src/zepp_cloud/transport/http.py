from __future__ import annotations

import logging
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

import httpx

_TRANSIENT_STATUS = {429, 500, 502, 503, 504}


def _redact_headers(headers: Mapping[str, str]) -> dict[str, str]:
    redacted = dict(headers)
    if redacted.get("apptoken"):
        redacted["apptoken"] = "***REDACTED***"
    return redacted


@dataclass
class HttpTransport:
    """httpx-based synchronous transport with retries and host pacing."""

    default_headers: Mapping[str, str]
    timeout: httpx.Timeout
    max_retries: int = 3
    backoff_base_seconds: float = 0.5
    rate_ms: int = 700
    logger: logging.Logger | None = None
    _client: httpx.Client | None = None
    _last_req_ms: dict[str, float] = field(default_factory=dict)
    _sleep: Callable[[float], None] = time.sleep

    def __post_init__(self) -> None:
        self._client = httpx.Client(timeout=self.timeout)

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None

    def __enter__(self) -> HttpTransport:
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        self.close()

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        json: Any = None,
        data: Any = None,
    ) -> httpx.Response:
        assert self._client is not None, "Transport has been closed"
        hdrs: dict[str, str] = {**self.default_headers}
        if headers:
            hdrs.update(headers)

        # Host-level pacing
        host = httpx.URL(url).host or ""
        if self.rate_ms > 0 and host:
            now_ms = time.time() * 1000.0
            last = self._last_req_ms.get(host)
            if last is not None:
                delta = now_ms - last
                wait_ms = self.rate_ms - delta
                if wait_ms > 0:
                    self._log_debug("pacing", host=host, wait_ms=wait_ms)
                    self._sleep(wait_ms / 1000.0)
            # refresh now to reduce tight loops
            self._last_req_ms[host] = time.time() * 1000.0
        else:
            # set first time to now
            self._last_req_ms[host] = time.time() * 1000.0

        attempt = 0
        while True:
            try:
                resp = self._client.request(
                    method,
                    url,
                    params=params,
                    headers=hdrs,
                    json=json,
                    data=data,
                )
            except httpx.TransportError as exc:  # includes timeouts
                if attempt >= self.max_retries:
                    raise
                attempt += 1
                delay = self._backoff_delay(attempt)
                self._log_debug(
                    "transport_error_retry",
                    attempt=attempt,
                    delay=delay,
                    error=str(exc),
                )
                self._sleep(delay)
                continue

            if resp.status_code in _TRANSIENT_STATUS and attempt < self.max_retries:
                attempt += 1
                delay = self._backoff_delay(attempt)
                self._log_debug(
                    "status_retry",
                    attempt=attempt,
                    delay=delay,
                    status=resp.status_code,
                    url=str(resp.request.url),
                )
                self._sleep(delay)
                continue

            return resp

    def _backoff_delay(self, attempt: int) -> float:
        # Exponential backoff with full jitter (0..base*2^attempt)
        max_delay = self.backoff_base_seconds * (2**attempt)
        return max_delay * 0.5  # deterministic mid-point to keep tests fast

    def _log_debug(self, msg: str, **kwargs: Any) -> None:
        if not self.logger:
            return
        safe = {k: ("***REDACTED***" if k.lower() == "apptoken" else v) for k, v in kwargs.items()}
        self.logger.debug(msg, extra={"zepp": safe})
