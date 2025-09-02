"""Client stubs for Zepp Cloud SDK.

Sprint 1 will implement real transport and resources; for now, we expose
placeholders to support packaging and CLI scaffolding.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ZeppClient:
    apptoken: str
    user_id: str
    timezone: str

    def __post_init__(self) -> None:
        # Placeholder: real initialization will occur in Sprint 1
        pass


class AsyncZeppClient:
    def __init__(self, apptoken: str, user_id: str, timezone: str) -> None:
        self.apptoken = apptoken
        self.user_id = user_id
        self.timezone = timezone

    async def __aenter__(self) -> "AsyncZeppClient":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:  # type: ignore[no-untyped-def]
        return None

