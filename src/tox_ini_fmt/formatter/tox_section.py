"""Formatting the core tox section."""

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Callable, Mapping

from packaging.requirements import Requirement
from packaging.version import Version

from .requires import requires
from .util import collect_multi_line, fix_and_reorder, to_boolean, to_list_of_env_values, to_py_dependencies

if TYPE_CHECKING:
    from configparser import ConfigParser, SectionProxy


def format_tox_section(parser: ConfigParser, pin_toxenvs: list[str]) -> None:
    """
    Format the core tox section.

    :param parser: the INI parser
    :param pin_toxenvs: environments to pin at start
    """
    if not parser.has_section("tox"):
        parser.add_section("tox")
    tox = parser["tox"]
    _handle_min_version(tox)
    tox.pop("isolated_build", None)

    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "min_version": str,
        "requires": to_py_dependencies,
        "provision_tox_env": str,
        "env_list": partial(to_list_of_env_values, pin_toxenvs),
        "package_env": str,
        "isolated_build_env": str,
        "no_package": to_boolean,
        "skip_missing_interpreters": to_boolean,
        "ignore_base_python_conflict": to_boolean,
    }
    upgrade = {
        "envlist": "env_list",
        "toxinidir": "tox_root",
        "toxworkdir": "work_dir",
        "skipsdist": "no_package",
        "isolated_build_env": "package_env",
        "setupdir": "package_root",
        "ignore_basepython_conflict": "ignore_base_python_conflict",
    }
    fix_and_reorder(parser, "tox", tox_section_cfg, upgrade)


def _handle_min_version(tox: SectionProxy) -> None:
    min_version = next((tox.pop(i) for i in ("minversion", "min_version") if i in tox), None)
    if min_version is None or int(min_version.split(".")[0]) < 4:  # noqa: PLR2004
        min_version = "4.2"
    tox_requires = [
        Requirement(i)
        for i in collect_multi_line(
            tox.get("requires", ""),
            line_split=None,
            normalize=lambda groups: {k: requires(v) for k, v in groups.items()},
        )[0]
    ]
    for _at, entry in enumerate(tox_requires):
        if entry.name == "tox":
            break
    else:
        _at = -1
    if _at == -1:
        tox_requires.append(Requirement(f"tox>={min_version}"))
    else:
        specifiers = list(tox_requires[_at].specifier)
        if len(specifiers) == 0 or Version(specifiers[0].version) < Version(min_version):
            tox_requires[_at] = Requirement(f"tox>={min_version}")
    tox["requires"] = "\n".join(str(i) for i in tox_requires)
