"""Utility methods."""

from __future__ import annotations

import itertools
import re
from collections import defaultdict
from functools import partial
from typing import TYPE_CHECKING, Callable, Mapping, TypedDict, cast

from .requires import requires

if TYPE_CHECKING:
    from configparser import ConfigParser


def to_boolean(payload: str) -> str:
    """
    Convert value to boolean.

    :param payload: the raw value
    :return: converted value
    """
    return "true" if payload.lower() == "true" else "false"


def fix_and_reorder(
    parser: ConfigParser,
    name: str,
    fix_cfg: Mapping[str, Callable[[str], str]],
    upgrade: dict[str, str],
) -> None:
    """
    Fix and reorder values.

    :param parser: the INI parser
    :param name:  name
    :param fix_cfg: values to fix
    :param upgrade: values to upgrade
    """
    section = parser[name]
    # upgrade
    for key, to in upgrade.items():
        if key in section:
            if to in section:
                msg = f"upgrade alias {to} also present for {key}"
                raise RuntimeError(msg)
            section[to] = section.pop(key)
    # normalize
    for key, fix in fix_cfg.items():
        if key in section:
            section[key] = fix(section[key])
    # reorder keys within section
    new_section = {k: section.pop(k) for k in fix_cfg if k in section}
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
    """
    Check if has substitute value.

    :param value: the raw value
    """
    match = RE_ITEM_REF.match(value)
    if match:
        sub_key = match.group("substitution_value")
        return sub_key.startswith("[") and "]" in sub_key
    return False


def to_list_of_env_values(pin_toxenvs: list[str], payload: str) -> str:
    """
    Expand list of tox envs.

    :param pin_toxenvs: envs to pin at top.
    :param payload: the tox envs list
    :return: the expanded tox env list

    Example:
    -------
    envlist = py39,py38
    envlist = {py37,py36}-django{20,21},{py37,py36}-mango{20,21},py38.

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
        elif char in {",", "\n"}:
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
    if last_entry:
        values.append(last_entry)
    # start with higher python version
    order_env_list(values, pin_toxenvs)
    # use newline instead of comma as separator, indent values one per newline (no value on key-row)
    return "\n{}".format("\n".join(f"{v}" for v in values))


_TOX_ENV_MATCHER = re.compile(r"((?P<major>\d)([.](?P<minor>\d+))?)|(?P<name>[a-zA-Z]*)(?P<version>\d*)")


class _ToxMatch(TypedDict):
    name: str
    version: int
    major: int
    minor: int


def _get_py_version(pin_toxenvs: list[str], env_list: str) -> tuple[int, ...]:
    for element in env_list.split("-"):
        if element in pin_toxenvs:
            return len(element) - pin_toxenvs.index(element), 0
        if match := _TOX_ENV_MATCHER.fullmatch(element):
            got = cast(_ToxMatch, {k: (v if k == "name" else int(v or 0)) for k, v in match.groupdict().items()})
            main = {"py": 0, "pypy": -1}.get(got.get("name") or "", -2)
            version: list[int] = [got["major"], got["minor"]] if got["major"] else [got["version"]]
            return main, *version
    return -3, 0


def order_env_list(values: list[str], pin_toxenvs: list[str]) -> None:
    """
    Order environment list.

    :param values: list of environments
    :param pin_toxenvs: values to pin at top
    """
    values.sort(key=partial(_get_py_version, pin_toxenvs), reverse=True)


CONDITIONAL_MARKER = re.compile(r"(?P<envs>[a-zA-Z0-9, ]+):(?P<value>.*)")


def collect_multi_line(
    value: str,
    line_split: str | None = r",| |\t",
    normalize: Callable[[dict[str, list[str]]], dict[str, list[str]]] | None = None,
    sort_key: Callable[[str], str] | None = None,
) -> tuple[list[str], list[str]]:
    """
    Collect multiline values.

    :param value:
    :param line_split:
    :param normalize:
    :param sort_key:
    :return:
    """
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
                    elif part not in groups[""]:  # remove duplicates
                        groups[""].append(part)
    normalized_group = normalize(groups) if normalize else groups
    result = list(
        itertools.chain.from_iterable(
            (f"{k}: {d}" if k else d for d in sorted(v, key=sort_key))
            for k, v in sorted(normalized_group.items(), key=lambda i: (len(i[0].split(", ")), i[0]))
        ),
    )
    return result, substitute


def to_py_dependencies(value: str) -> str:
    """
    Format to list Python dependencies.

    :param value: the raw value
    :return: the formatted value
    """
    raw_deps, substitute = collect_multi_line(
        value,
        line_split=None,
        normalize=lambda groups: {k: requires(v) for k, v in groups.items()},
        sort_key=lambda _: "",  # we already sorted as we wanted in normalize, keep it as is
    )
    return fmt_list(raw_deps, substitute)


def fmt_list(values: list[str], substitute: list[str]) -> str:
    """
    Format a list of values.

    :param values: the raw values
    :param substitute: substitution
    :return: formatted list
    """
    return "\n".join(["", *sorted(substitute), *values])
