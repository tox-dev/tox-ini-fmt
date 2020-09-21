import re
from configparser import ConfigParser
from typing import Callable, List, Mapping, Tuple

from .util import fix_and_reorder, to_boolean


def format_tox_section(parser: ConfigParser) -> None:
    if not parser.has_section("tox"):
        return
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "envlist": to_list_of_env_values,
        "isolated_build": to_boolean,
        "skipsdist": to_boolean,
        "skip_missing_interpreters": to_boolean,
        "minversion": str,
    }
    fix_and_reorder(parser, "tox", tox_section_cfg)


def to_list_of_env_values(payload: str) -> str:
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
            order_env_list(envs)
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
    values.append(cur_str.strip())
    # start with higher python version
    order_env_list(values)
    # use newline instead of coma as separator, indent values one per newline (no value on key-row)
    result = "\n{}".format("\n".join(f"{v}" for v in values))
    return result


def order_env_list(values: List[str]) -> None:
    values.sort(key=_get_py_version, reverse=True)


def _get_py_version(env_list: str) -> Tuple[int, int]:
    for element in env_list.split("-"):
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
    return 0, 0


_MATCHER = re.compile(r"^([a-zA-Z]*)(\d*)$")
