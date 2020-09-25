import re
from configparser import ConfigParser
from typing import Callable, List, Mapping, Set

from .requires import requires
from .util import fix_and_reorder, to_boolean, to_multiline


def format_test_env(parser: ConfigParser, name: str) -> None:
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "description": str,
        "passenv": to_pass_env,
        "setenv": to_set_env,
        "basepython": str,
        "skip_install": to_boolean,
        "deps": to_deps,
        "extras": to_extras,
        "commands": to_multiline,
    }
    fix_and_reorder(parser, name, tox_section_cfg)


def fmt_list(values: List[str]) -> str:
    return "\n".join([""] + values)


def to_deps(value: str) -> str:
    return fmt_list(requires(value))


def to_extras(value: str) -> str:
    """Must be a line separated list - fix comma separated format"""
    return fmt_list(line_list(value))


def line_list(value: str) -> List[str]:
    collected: Set[str] = set()
    for val in value.splitlines():
        for a_val in re.split(r",| |\t", val.strip()):
            if a_val.strip():
                collected.add(a_val.strip())
    return list(sorted(collected))


def to_pass_env(value: str) -> str:
    return fmt_list(line_list(value))


def to_set_env(value: str) -> str:
    values: List[str] = []
    for line in value.splitlines():
        line = line.strip()
        if line:
            at = line.find("=")
            values.append(f"{line[:at].strip()} = {line[at+1:].strip()}")
    return fmt_list(sorted(values))
