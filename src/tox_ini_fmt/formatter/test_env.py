from __future__ import annotations

import itertools
import re
from collections import defaultdict
from configparser import ConfigParser
from typing import Callable, Mapping

from .requires import requires
from .util import fix_and_reorder, is_substitute, to_boolean


def format_test_env(parser: ConfigParser, name: str) -> None:
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "description": str,
        "passenv": to_pass_env,
        "setenv": to_set_env,
        "basepython": str,
        "skip_install": to_boolean,
        "usedevelop": to_boolean,
        "deps": to_deps,
        "extras": to_extras,
        "parallel_show_output": to_boolean,
        "changedir": str,
        "commands": to_commands,
    }
    fix_and_reorder(parser, name, tox_section_cfg)


CONDITIONAL_MARKER = re.compile(r"(?P<envs>[a-zA-Z0-9,]+):(?P<value>.*)")


def to_deps(value: str) -> str:
    raw_deps, substitute = collect_multi_line(value, line_split=None)
    groups = defaultdict(list)
    for dep in raw_deps:
        if dep.startswith("-r"):
            groups["-r"].append(dep)
        else:
            match = CONDITIONAL_MARKER.match(dep)
            if match:
                elements = match.groupdict()
                groups[",".join(sorted(elements["envs"].split(",")))].append(elements["value"].strip())
            else:
                groups[""].append(dep)
    groups_requires = {key: requires(value) for key, value in groups.items()}
    deps = list(
        itertools.chain.from_iterable(
            (f"{k}: {d}" if k not in ("", "-r") else d for d in v) for k, v in sorted(groups_requires.items())
        )
    )
    return fmt_list(deps, substitute)


def collect_multi_line(value: str, line_split: str | None = r",| |\t") -> tuple[list[str], list[str]]:
    lines = value.strip().splitlines()
    substitute, elements = [], []
    for line in lines:
        for part in re.split(line_split, line.strip()) if line_split else [line.strip()]:
            if part:  # remove empty lines
                if is_substitute(part):
                    substitute.append(part)
                else:
                    if part not in elements:  # remove duplicates
                        elements.append(part)
    return elements, substitute


def fmt_list(values: list[str], substitute: list[str]) -> str:
    return "\n".join([""] + substitute + values)


def to_extras(value: str) -> str:
    """Must be a line separated list - fix comma separated format"""
    extras, substitute = collect_multi_line(value)
    return fmt_list(sorted(extras), substitute)


def to_pass_env(value: str) -> str:
    pass_env, substitute = collect_multi_line(value)
    return fmt_list(sorted(pass_env), substitute)


def to_set_env(value: str) -> str:
    raw_set_env, substitute = collect_multi_line(value, line_split=None)
    set_env: list[str] = []
    for env in raw_set_env:
        at = env.find("=")
        if at == -1:
            raise RuntimeError(f"invalid line {env} in setenv")
        set_env.append(f"{env[:at].strip()} = {env[at+1:].strip()}")
    return fmt_list(sorted(set_env), substitute)


_CMD_SEP = "\\"


def to_commands(value: str) -> str:
    result: list[str] = []
    ends_with_sep = False
    for val in value.splitlines():
        val = val.strip()
        cur_ends_with_sep = val.endswith(_CMD_SEP)
        if cur_ends_with_sep:
            val = val[:-1].strip()
        if val and val != _CMD_SEP:
            ending = f" {_CMD_SEP}" if cur_ends_with_sep else ""
            prepend = "  " if ends_with_sep else ""
            result.append(f"{prepend}{val}{ending}")
            ends_with_sep = cur_ends_with_sep
    return fmt_list(result, [])
