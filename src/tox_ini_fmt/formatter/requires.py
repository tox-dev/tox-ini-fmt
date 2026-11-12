"""Normalize requires values."""

from __future__ import annotations

from packaging.requirements import InvalidRequirement, Requirement
from packaging.specifiers import SpecifierSet


def requires(raws: list[str]) -> list[str]:
    """
    Normalize a list of requires.

    :param raws: the raw values
    :returns: the formatted values
    """
    return sorted((_normalize_req(req) for req in raws if req), key=lambda req: (";" in req, _req_name(req), req))


def _normalize_req(req: str) -> str:
    try:
        parsed = Requirement(req)
    except InvalidRequirement:
        return req

    normalized = []
    for spec in parsed.specifier:
        version = spec.version
        if spec.operator in {">=", "=="}:
            while version.endswith(".0"):
                version = version[:-2]
        normalized.append(f"{spec.operator}{version}")
    parsed.specifier = SpecifierSet(",".join(normalized))
    return str(parsed)


def _req_name(req: str) -> str:
    try:
        return Requirement(req).name
    except InvalidRequirement:
        return req


__all__ = [
    "requires",
]
