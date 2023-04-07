from __future__ import annotations

from packaging.requirements import InvalidRequirement, Requirement


def normalize_req(req: str) -> str:
    try:
        parsed = Requirement(req)
    except InvalidRequirement:
        return req

    for spec in parsed.specifier:
        if spec.operator in (">=", "=="):
            version = spec.version
            while version.endswith(".0"):
                version = version[:-2]
                spec._spec = (spec._spec[0], version)
    return str(parsed)


def _req_name(req: str) -> str:
    try:
        return Requirement(req).name
    except InvalidRequirement:
        return req


def requires(raws: list[str]) -> list[str]:
    values = (normalize_req(req) for req in raws if req)
    normalized = sorted(values, key=lambda req: (";" in req, _req_name(req), req))
    return normalized


__all__ = [
    "requires",
]
