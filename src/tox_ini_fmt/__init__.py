"""Format tox.ini files."""

from __future__ import annotations

__lazy_modules__ = [f"{__spec__.parent}.version"]  # ty: ignore[missing-union-attribute]  # imported modules have a spec

from .version import __version__

__all__ = [
    "__version__",
]
