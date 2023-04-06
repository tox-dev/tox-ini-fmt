from __future__ import annotations

from configparser import ConfigParser
from functools import partial
from typing import Callable, Mapping

from .util import fix_and_reorder, to_boolean, to_list_of_env_values, to_py_dependencies


def format_tox_section(parser: ConfigParser, pin_toxenvs: list[str]) -> None:
    if not parser.has_section("tox"):
        return
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "minversion": str,
        "min_version": str,
        "requires": to_py_dependencies,
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
