from __future__ import annotations

import itertools
from configparser import ConfigParser

from .util import order_env_list


def order_sections(parser: ConfigParser, pin_toxenvs: list[str]) -> None:
    """
    Start with tox, then testenv. The testenv elements follow the order within envlist. Then all other testenv elements,
    and end it with any other sections present in the file (e.g. pytest/mypy configuration).
    """
    order = ["tox", "testenv"]
    order.extend(f"testenv:{env}" for env in load_and_order_env_list(parser, pin_toxenvs))
    order.extend(s for s in parser.sections() if s not in order and s.startswith("testenv:"))
    order.extend(s for s in parser.sections() if s not in order and not s.startswith("testenv:"))
    sections: dict[str, dict[str, str]] = {}
    for section in order:
        if parser.has_section(section):
            sections[section] = dict(parser[section])
            parser.pop(section)
    for k, v in sections.items():
        parser[k] = v


def load_and_order_env_list(parser: ConfigParser, pin_toxenvs: list[str]) -> list[str]:
    result: list[str] = next(
        (explode_env_list(parser["tox"][i]) for i in ("envlist", "env_list") if i in parser["tox"]),
        [],
    )
    missing = [e for e in pin_toxenvs if e not in result]
    if missing:
        raise RuntimeError(f"missing tox environment(s) to pin {', '.join(missing)}")
    order_env_list(result, pin_toxenvs)
    return result


def explode_env_list(env_list: str) -> list[str]:
    result: list[str] = []
    for entry in env_list.split("\n"):
        entry = entry.strip()
        if entry:
            parts = []
            for part in entry.split("-"):
                if part[0] == "{" and part[-1] == "}":
                    sub_part = part[1:-1]
                else:
                    sub_part = part
                sub_parts = [i.strip() for i in sub_part.split(",")]
                parts.append(sub_parts)
            result.extend("-".join(i).strip("-") for i in itertools.product(*parts))
    return result
