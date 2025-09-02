"""Zepp Cloud Python SDK package."""

try:
    from ._version import version as __version__  # type: ignore
except Exception:  # pragma: no cover - fallback during editable dev
    __version__ = "0.0.0.dev0"

__all__ = ["__version__"]

