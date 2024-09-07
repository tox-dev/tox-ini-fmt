"""Normalize requires values."""

from __future__ import annotations

from packaging.requirements import InvalidRequirement, Requirement


def normalize_req(req: str) -> str:
    try:
        parsed = Requirement(req)
    except InvalidRequirement:
        return req

    for spec in parsed.specifier:
        if spec.operator in {">=", "=="}:
            version = spec.version
            while version.endswith(".0"):
                version = version[:-2]
                spec._spec = (spec._spec[0], version)  # noqa: SLF001
    return str(parsed)


def _req_name(req: str) -> str:
    try:
        return Requirement(req).name
    except InvalidRequirement:
        return req


def requires(raws: list[str]) -> list[str]:
    """
    Normalize a list of requires.

    :param raws: the raw values
    :return: the formatted values
    """
    values = (normalize_req(req) for req in raws if req)
    return sorted(values, key=lambda req: (";" in req, _req_name(req), req))


__all__ = [
    "requires",
]
