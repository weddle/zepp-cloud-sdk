"""Auth utilities for Zepp Cloud SDK."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AppTokenAuth:
    """Simple app token auth container.

    This is a placeholder for future transport integration.
    """

    apptoken: str
