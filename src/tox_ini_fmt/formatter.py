from collections import Mapping
from configparser import ConfigParser
from io import StringIO
from pathlib import Path
from typing import Callable


def format_tox_ini(tox_ini: Path) -> str:
    parser = ConfigParser()
    with tox_ini.open("rt"):
        parser.read([tox_ini])

    format_tox_section(parser)

    output = StringIO()
    parser.write(output)
    result = output.getvalue().strip() + "\n"
    result = result.replace("\t", "  ")
    result = result.replace(" \n", "\n")
    return result


def format_tox_section(parser: ConfigParser) -> None:
    if not parser.has_section("tox"):
        return
    tox_section = parser["tox"]
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "envlist": _list_of_env_values,
        "isolated_build": _boolean,
        "skipsdist": _boolean,
        "skip_missing_interpreters": _boolean,
        "minversion": str,
    }
    for key, fix in tox_section_cfg.items():
        if key in tox_section:
            tox_section[key] = fix(tox_section[key])

    # reorder keys within section
    new_section = {k: tox_section.pop(k) for k in tox_section_cfg.keys() if k in tox_section}
    new_section.update(sorted(tox_section.items()))  # sort any remaining keys
    parser["tox"] = new_section


def _list_of_env_values(payload: str) -> str:
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
            cur_str += f'{{{", ".join(i.strip() for i in brace_str[1:].split(","))}}}'
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
    # use newline instead of coma as separator, indent values one per newline (no value on key-row)
    result = "\n{}".format("\n".join(f"{v}" for v in values))
    return result


def _boolean(payload: str) -> str:
    return "true" if payload.lower() == "true" else "false"
