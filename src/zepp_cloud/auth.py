"""Auth utilities for Zepp Cloud SDK."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from dataclasses import dataclass


@dataclass(frozen=True)
class AppTokenAuth:
    """Simple app token auth container.

    This is a placeholder for future transport integration.
    """

    apptoken: str

    def apply(self, headers: MutableMapping[str, str]) -> None:
        """Inject the apptoken header into the provided header mapping."""
        headers["apptoken"] = self.apptoken

    def headers(self) -> Mapping[str, str]:
        """Return headers representing this auth.

        Useful when constructing transports.
        """
        return {"apptoken": self.apptoken}
