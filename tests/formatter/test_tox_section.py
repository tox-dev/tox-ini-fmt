from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from tox_ini_fmt.formatter import format_tox_ini
from tox_ini_fmt.formatter.tox_section import order_env_list


def test_no_tox_section(tox_ini: Path) -> None:
    tox_ini.write_text("")
    assert format_tox_ini(tox_ini) == "\n"


def test_format_envlist_simple(tox_ini: Path) -> None:
    tox_ini.write_text("[tox]\nenvlist=py39,py38\n")
    outcome = format_tox_ini(tox_ini)
    assert outcome == "[tox]\nenvlist =\n    py39\n    py38\n"


def test_format_envlist_start_newline(tox_ini: Path) -> None:
    ok = "[tox]\nenvlist =\n    py39\n    py38\n"
    tox_ini.write_text(ok)
    outcome = format_tox_ini(tox_ini)
    assert outcome == ok


def test_format_envlist_generator(tmp_path: Path) -> None:
    path = tmp_path / "tox.ini"
    path.write_text("[tox]\nenvlist={py36,py37}-django{20,21},{py36,py37}-mango{20,21},py38\n")
    outcome = format_tox_ini(path)
    assert outcome == "[tox]\nenvlist =\n    py38\n    {py37, py36}-django{21, 20}\n    {py37, py36}-mango{21, 20}\n"


def test_tox_section_order(tox_ini: Path) -> None:
    text = """
    [tox]
    skip_missing_interpreters=true
    isolated_build=true
    requires=
     tox-magic >= 0.2
     tox-abc >= 0.1
    minversion=3.14
    skipsdist=false
    envlist=py37
    """
    tox_ini.write_text(dedent(text))
    outcome = format_tox_ini(tox_ini)
    result = """\
    [tox]
    minversion = 3.14
    requires =
        tox-abc>=0.1
        tox-magic>=0.2
    envlist =
        py37
    isolated_build = true
    skipsdist = false
    skip_missing_interpreters = true
    """
    result = dedent(result)
    assert outcome == result


@pytest.mark.parametrize(
    "key",
    [
        "isolated_build",
        "skipsdist",
        "skip_missing_interpreters",
    ],
)
@pytest.mark.parametrize(
    ("value", "result"),
    [
        ("True", "true"),
        ("False", "false"),
        ("TRUE", "true"),
        ("FALSE", "false"),
    ],
)
def test_tox_fmt_boolean(tox_ini: Path, key: str, value: str, result: str) -> None:
    tox_ini.write_text(f"[tox]\n{key}={value}")
    outcome = format_tox_ini(tox_ini)
    expected = f"[tox]\n{key} = {result}\n"
    assert outcome == expected


@pytest.mark.parametrize(
    ("arg", "outcome"),
    [
        ([], []),
        (["py38", "py37"], ["py38", "py37"]),
        (["py37", "py38"], ["py38", "py37"]),
        (["py", "py37", "pypy3", "py38", "pypy2", "pypy"], ["py38", "py37", "py", "pypy3", "pypy2", "pypy"]),
        (["py38-dpkg", "py38", "py37-dpkg", "py37"], ["py38-dpkg", "py38", "py37-dpkg", "py37"]),
        (["py37-dpkg", "py37", "py38-dpkg", "py38"], ["py38-dpkg", "py38", "py37-dpkg", "py37"]),
        (["py37", "py37-dpkg", "py38", "py38-dpkg"], ["py38", "py38-dpkg", "py37", "py37-dpkg"]),
        (["Jython", "jython36", "jython", "Jython27", "py38"], ["py38", "jython36", "Jython27", "Jython", "jython"]),
    ],
)
def test_order_env_list(arg: list[str], outcome: list[str]) -> None:
    order_env_list(arg, [])
    assert arg == outcome


def test_format_tox_ini_handles_trailing_comma(tox_ini: Path) -> None:
    """tox.ini gets formatted without adding additional whitespace

    This was previously caused by a trailing comma in the `envlist`.
    """
    tox_ini.write_text("[tox]\nenvlist=\n    py38,\n    pkg,\n" "[testenv:pkg]\na=b\n")
    result = format_tox_ini(tox_ini)
    assert result == "[tox]\nenvlist =\n    py38\n    pkg\n\n[testenv:pkg]\na = b\n"
