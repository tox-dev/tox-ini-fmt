from configparser import ConfigParser
from typing import Callable, Mapping

from .requires import requires
from .util import fix_and_reorder, to_multiline


def format_test_env(parser: ConfigParser, name: str) -> None:
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "description": str,
        "basepython": str,
        "deps": to_deps,
        "extras": str,
        "commands": to_multiline,
    }
    fix_and_reorder(parser, name, tox_section_cfg)


def to_deps(value: str) -> str:
    deps = requires(value)
    deps.insert(0, "")
    return "\n".join(deps)
