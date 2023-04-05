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
        "runner": str,
        "description": str,
        "base_python": str,
        "basepython": str,
        "system_site_packages": to_boolean,
        "sitepackages": to_boolean,
        "always_copy": to_boolean,
        "alwayscopy": to_boolean,
        "download": to_boolean,
        "package": str,
        "package_env": str,
        "wheel_build_env": str,
        "package_tox_env_type": str,
        "package_root": str,
        "skip_install": to_boolean,
        "use_develop": to_boolean,
        "usedevelop": to_boolean,
        "meta_dir": str,
        "pkg_dir": str,
        "pip_pre": to_boolean,
        "deps": to_deps,
        "extras": to_ordered_list,
        "recreate": to_boolean,
        "parallel_show_output": to_boolean,
        "pass_env": to_pass_env,
        "passenv": to_pass_env,
        "set_env": to_set_env,
        "setenv": to_set_env,
        "change_dir": str,
        "changedir": str,
        "args_are_paths": to_boolean,
        "ignore_errors": to_boolean,
        "ignore_outcome": to_boolean,
        "commands_pre": to_commands,
        "commands": to_commands,
        "commands_post": to_commands,
        "allowlist_externals": to_ordered_list,
        "suicide_timeout": str,
        "interrupt_timeout": str,
        "terminate_timeout": str,
        "depends": to_ordered_list,
    }
    fix_and_reorder(parser, name, tox_section_cfg)


CONDITIONAL_MARKER = re.compile(r"(?P<envs>[a-zA-Z0-9, ]+):(?P<value>.*)")


def to_deps(value: str) -> str:
    raw_deps, substitute = collect_multi_line(
        value,
        line_split=None,
        normalize=lambda groups: {k: requires(v) for k, v in groups.items()},
    )
    return fmt_list(raw_deps, substitute)


def collect_multi_line(
    value: str,
    line_split: str | None = r",| |\t",
    normalize: Callable[[dict[str, list[str]]], dict[str, list[str]]] | None = None,
) -> tuple[list[str], list[str]]:
    groups: defaultdict[str, list[str]] = defaultdict(list)
    substitute: list[str] = []
    for line in value.strip().splitlines():
        match = CONDITIONAL_MARKER.match(line)
        if match:
            elements = match.groupdict()
            normalized_key = ", ".join(sorted(i.strip() for i in elements["envs"].split(",")))
            groups[normalized_key].append(elements["value"].strip())
        else:
            for part in re.split(line_split, line.strip()) if line_split else [line.strip()]:
                if part:  # remove empty lines
                    if is_substitute(part):
                        substitute.append(part)
                    else:
                        if part not in groups[""]:  # remove duplicates
                            groups[""].append(part)
    normalized_group = normalize(groups) if normalize else groups
    result = list(
        itertools.chain.from_iterable(
            sorted(f"{k}: {d}" if k != "" else d for d in v)
            for k, v in sorted(normalized_group.items(), key=lambda i: (len(i[0].split(", ")), i[0]))
        ),
    )
    return result, substitute


def fmt_list(values: list[str], substitute: list[str]) -> str:
    return "\n".join([""] + sorted(substitute) + values)


def to_ordered_list(value: str) -> str:
    """Must be a line separated list - fix comma separated format"""
    extras, substitute = collect_multi_line(value)
    return fmt_list(extras, substitute)


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
