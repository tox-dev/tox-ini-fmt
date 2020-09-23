import re
from typing import List

BASE_NAME_REGEX = re.compile(r"[^!=><\s@]+")
REQ_REGEX = re.compile(r"(===|==|!=|~=|>=?|<=?|@)\s*([^,]+)")


def requires(raw: str) -> List[str]:
    require_group = raw.strip().splitlines()
    if not require_group:
        return []
    values = (_normalize_req(req) for req in require_group)
    normalized = sorted(values, key=lambda req: (";" in req, _req_base(req), req))
    return normalized


def _normalize_req(req: str) -> str:
    lib, _, envs = req.partition(";")
    normalized = _normalize_lib(lib)
    envs = envs.strip()
    if not envs:
        return normalized
    return f"{normalized};{envs}"


def _normalize_lib(lib: str) -> str:
    base = _req_base(lib)
    values = sorted(
        (f"{m.group(1)}{m.group(2)}" for m in REQ_REGEX.finditer(lib)),
        key=lambda c: ("<" in c, ">" in "c", c),
    )
    if values:  # strip .0 version
        while values[0].endswith(".0"):
            values[0] = values[0][:-2]
    return f"{base}{','.join(values)}"


def _req_base(lib: str) -> str:
    match = re.match(BASE_NAME_REGEX, lib)
    if match is None:
        raise ValueError(lib)
    return match.group(0)
