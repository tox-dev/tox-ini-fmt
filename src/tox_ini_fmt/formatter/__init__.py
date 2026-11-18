"""Logic related to formatting the file."""

from __future__ import annotations

__lazy_modules__ = [f"{__spec__.parent}.tox_ini"]  # ty: ignore[missing-union-attribute]  # imported modules have a spec

from .tox_ini import format_tox_ini

__all__ = [
    "format_tox_ini",
]
