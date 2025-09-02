"""Client stubs for Zepp Cloud SDK.

Sprint 1 will implement real transport and resources; for now, we expose
placeholders to support packaging and CLI scaffolding.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import httpx

from .auth import AppTokenAuth
from .config import ZeppConfig
from .transport.http import HttpTransport


@dataclass
class ZeppClient:
    apptoken: str
    user_id: str
    timezone: str
    config: ZeppConfig = field(default_factory=ZeppConfig)
    _transport: HttpTransport | None = None

    def __post_init__(self) -> None:
        auth = AppTokenAuth(self.apptoken)
        default_headers = {
            "apptoken": auth.apptoken,
            "appPlatform": self.config.app_platform,
            "appname": self.config.app_name,
            "User-Agent": self.config.user_agent,
        }
        timeout = self._build_timeout()
        self._transport = HttpTransport(
            default_headers=default_headers,
            timeout=timeout,
            max_retries=self.config.max_retries,
            backoff_base_seconds=self.config.backoff_base_seconds,
            rate_ms=self.config.rate_ms,
        )

    def _build_timeout(self) -> httpx.Timeout:
        return httpx.Timeout(
            timeout=self.config.timeout_total,
            connect=self.config.timeout_connect,
            read=self.config.timeout_read,
        )

    def close(self) -> None:
        if self._transport:
            self._transport.close()


class AsyncZeppClient:
    def __init__(self, apptoken: str, user_id: str, timezone: str) -> None:
        self.apptoken = apptoken
        self.user_id = user_id
        self.timezone = timezone

    async def __aenter__(self) -> AsyncZeppClient:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        return None
