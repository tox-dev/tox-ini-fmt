"""Order configuration sections."""

from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

from .values import order_env_list

if TYPE_CHECKING:
    from configparser import ConfigParser


def order_sections(parser: ConfigParser, pin_toxenvs: list[str]) -> None:
    """
    Order sections.

    :param parser: the INI parsers
    :param pin_toxenvs: envs to pin
    """
    # Start with tox, then testenv. The testenv elements follow the order within envlist. Then all other testenv
    # elements and end it with any other sections present in the file (e.g. pytest/mypy configuration).
    order = ["tox", "testenv"]
    order.extend(f"testenv:{env}" for env in _load_and_order_env_list(parser, pin_toxenvs))
    order.extend(s for s in parser.sections() if s not in order and s.startswith("testenv:"))
    order.extend(s for s in parser.sections() if s not in order and not s.startswith("testenv:"))
    sections: dict[str, dict[str, str]] = {}
    for section in order:
        if parser.has_section(section):
            sections[section] = dict(parser[section])
            parser.pop(section)
    for name, options in sections.items():
        parser[name] = options


def _load_and_order_env_list(parser: ConfigParser, pin_toxenvs: list[str]) -> list[str]:
    # Load and order tox env list.
    #
    # :param parser: the INI parser
    # :param pin_toxenvs: envs to pint at the top
    # :returns: the expanded and ordered list.
    # :raises RuntimeError:
    result: list[str] = next(
        (explode_env_list(parser["tox"][i]) for i in ("envlist", "env_list") if i in parser["tox"]),
        [],
    )
    if missing := [e for e in pin_toxenvs if e not in result]:
        msg = f"missing tox environment(s) to pin {', '.join(missing)}"
        raise RuntimeError(msg)
    order_env_list(result, pin_toxenvs)
    return result


def explode_env_list(env_list: str) -> list[str]:
    """
    Explode a tox env list.

    :param env_list: the raw value
    :returns: exploded representation
    """
    result: list[str] = []
    for raw_entry in env_list.split("\n"):
        if entry := raw_entry.strip():
            parts = []
            for part in entry.split("-"):
                sub_part = part[1:-1] if part[0] == "{" and part[-1] == "}" else part
                parts.append([i.strip() for i in sub_part.split(",")])
            result.extend("-".join(i).strip("-") for i in itertools.product(*parts))
    return result


__all__ = [
    "explode_env_list",
    "order_sections",
]
