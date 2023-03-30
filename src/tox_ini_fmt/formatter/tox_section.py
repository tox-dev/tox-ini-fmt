from __future__ import annotations

import re
from configparser import ConfigParser
from functools import partial
from typing import Callable, Mapping

from .requires import requires
from .test_env import collect_multi_line, fmt_list
from .util import fix_and_reorder, to_boolean


def format_tox_section(parser: ConfigParser, pin_toxenvs: list[str]) -> None:
    if not parser.has_section("tox"):
        return
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "minversion": str,
        "min_version": str,
        "requires": to_requires,
        "provision_tox_env": str,
        "env_list": partial(to_list_of_env_values, pin_toxenvs),
        "envlist": partial(to_list_of_env_values, pin_toxenvs),
        "isolated_build": to_boolean,
        "package_env": str,
        "isolated_build_env": str,
        "no_package": to_boolean,
        "skipsdist": to_boolean,
        "skip_missing_interpreters": to_boolean,
        "ignore_base_python_conflict": to_boolean,
        "ignore_basepython_conflict": to_boolean,
    }
    fix_and_reorder(parser, "tox", tox_section_cfg)


def to_requires(value: str) -> str:
    raw_deps, substitute = collect_multi_line(value, line_split=None)
    return fmt_list(requires(raw_deps), substitute)


def to_list_of_env_values(pin_toxenvs: list[str], payload: str) -> str:
    """
    Example:

    envlist = py39,py38
    envlist = {py37,py36}-django{20,21},{py37,py36}-mango{20,21},py38
    """
    within_braces, values = False, []
    cur_str, brace_str = "", ""
    for char in payload:
        if char == "{":
            within_braces = True
        elif char == "}":
            within_braces = False
            envs = [i.strip() for i in brace_str[1:].split(",")]
            order_env_list(envs, pin_toxenvs)
            cur_str += f'{{{", ".join(envs)}}}'
            brace_str = ""
            continue
        elif char in (",", "\n"):
            if within_braces:
                pass
            else:
                to_add = cur_str.strip()
                if to_add:
                    values.append(to_add)
                cur_str = ""
                continue
        if within_braces:
            brace_str += char
        else:
            cur_str += char
    # avoid adding an empty value, caused e.g. by a trailing comma
    last_entry = cur_str.strip()
    if last_entry != "":
        values.append(last_entry)
    # start with higher python version
    order_env_list(values, pin_toxenvs)
    # use newline instead of comma as separator, indent values one per newline (no value on key-row)
    result = "\n{}".format("\n".join(f"{v}" for v in values))
    return result


def order_env_list(values: list[str], pin_toxenvs: list[str]) -> None:
    values.sort(key=partial(_get_py_version, pin_toxenvs), reverse=True)


_MATCHER = re.compile(r"^([a-zA-Z]*)(\d*)$")


def _get_py_version(pin_toxenvs: list[str], env_list: str) -> tuple[int, int]:
    for element in env_list.split("-"):
        if element in pin_toxenvs:
            return len(element) - pin_toxenvs.index(element), 0
        match = _MATCHER.match(element)
        if match is not None:
            name, version = match.groups()
            name = name.lower()
            if name == "py":
                main = 0
            elif name == "pypy":
                main = -1
            else:
                main = -2
            return main, int(version) if version else 0
    return -3, 0
