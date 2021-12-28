from __future__ import annotations

import re
from configparser import ConfigParser
from typing import Callable, Mapping


def to_boolean(payload: str) -> str:
    return "true" if payload.lower() == "true" else "false"


def fix_and_reorder(parser: ConfigParser, name: str, fix_cfg: Mapping[str, Callable[[str], str]]) -> None:
    section = parser[name]
    for key, fix in fix_cfg.items():
        if key in section:
            section[key] = fix(section[key])
    # reorder keys within section
    new_section = {k: section.pop(k) for k in fix_cfg.keys() if k in section}
    new_section.update(sorted(section.items()))  # sort any remaining keys
    parser[name] = new_section


RE_ITEM_REF = re.compile(
    r"""
        (?<!\\)[{]
        (?:(?P<sub_type>[^[:{}]+):)?    # optional sub_type for special rules
        (?P<substitution_value>(?:\[[^,{}]*\])?[^:,{}]*)  # substitution key
        (?::(?P<default_value>[^{}]*))?   # default value
        [}]
        """,
    re.VERBOSE,
)


def is_substitute(value: str) -> bool:
    match = RE_ITEM_REF.match(value)
    if match:
        sub_key = match.group("substitution_value")
        return sub_key.startswith("[") and "]" in sub_key
    return False
