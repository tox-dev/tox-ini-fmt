from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from .values import (
    collect_multi_line,
    fix_and_reorder,
    fmt_list,
    to_boolean,
    to_list_of_env_values,
    to_py_dependencies,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping
    from configparser import ConfigParser


def format_test_env(parser: ConfigParser, name: str) -> None:
    tox_section_cfg: Mapping[str, Callable[[str], str]] = {
        "runner": str,
        "description": str,
        "base_python": str,
        "system_site_packages": to_boolean,
        "always_copy": to_boolean,
        "download": to_boolean,
        "package": str,
        "package_env": str,
        "wheel_build_env": str,
        "package_tox_env_type": str,
        "package_root": str,
        "skip_install": to_boolean,
        "meta_dir": str,
        "pkg_dir": str,
        "pip_pre": to_boolean,
        "deps": to_py_dependencies,
        "extras": to_ordered_list,
        "recreate": to_boolean,
        "parallel_show_output": to_boolean,
        "pass_env": _to_pass_env,
        "set_env": _to_set_env,
        "setenv": _to_set_env,
        "change_dir": str,
        "args_are_paths": to_boolean,
        "ignore_errors": to_boolean,
        "ignore_outcome": to_boolean,
        "commands_pre": _to_commands,
        "commands": _to_commands,
        "commands_post": _to_commands,
        "allowlist_externals": to_ordered_list,
        "suicide_timeout": str,
        "interrupt_timeout": str,
        "terminate_timeout": str,
        "depends": partial(to_list_of_env_values, []),
    }

    section = parser[name]
    if to_boolean(next((section.pop(i) for i in ("usedevelop", "use_develop") if i in section), "false")) == "true":
        parser[name]["package"] = "editable"

    upgrade = {
        "alwayscopy": "always_copy",
        "basepython": "base_python",
        "changedir": "change_dir",
        "envbindir": "env_bin_dir",
        "envdir": "env_dir",
        "envlogdir": "env_log_dir",
        "envname": "env_name",
        "envsitepackagesdir": "env_site_packages_dir",
        "envtmpdir": "env_tmp_dir",
        "ignore_basepython_conflict": "ignore_base_python_conflict",
        "isolated_build_env": "package_env",
        "passenv": "pass_env",
        "setenv": "set_env",
        "setupdir": "package_root",
        "sitepackages": "system_site_packages",
        "skipsdist": "no_package",
    }
    fix_and_reorder(parser, name, tox_section_cfg, upgrade)


def to_ordered_list(value: str) -> str:
    extras, substitute = collect_multi_line(value)
    return fmt_list(extras, substitute)


def _to_pass_env(value: str) -> str:
    pass_env, substitute = collect_multi_line(value)
    return fmt_list(sorted(pass_env), substitute)


def _to_set_env(value: str) -> str:
    raw_set_env, substitute = collect_multi_line(value, line_split=None)
    set_env: list[str] = []
    for env in raw_set_env:
        if env.strip().startswith("file|"):
            set_env.append(env.strip())
            continue

        at = env.find("=")
        if at == -1:
            msg = f"invalid line {env} in setenv"
            raise RuntimeError(msg)
        set_env.append(f"{env[:at].strip()} = {env[at + 1 :].strip()}")
    return fmt_list(sorted(set_env), substitute)


def _to_commands(value: str) -> str:
    result: list[str] = []
    cmd_sep: str = "\\"
    ends_with_sep = False
    for raw_val in value.splitlines():
        val = raw_val.strip()
        cur_ends_with_sep = val.endswith(cmd_sep)
        if cur_ends_with_sep:
            val = val[:-1].strip()
        if val and val != cmd_sep:
            line = f"{'  ' if ends_with_sep else ''}{val}"
            result.append(f"{line} {cmd_sep}" if cur_ends_with_sep else line)
            ends_with_sep = cur_ends_with_sep
    return fmt_list(result, [])


__all__ = [
    "format_test_env",
    "to_ordered_list",
]
