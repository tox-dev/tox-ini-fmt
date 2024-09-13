from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from tox_ini_fmt.formatter import format_tox_ini
from tox_ini_fmt.formatter.util import order_env_list

if TYPE_CHECKING:
    from pathlib import Path


def test_no_tox_section(tox_ini: Path) -> None:
    tox_ini.write_text("")
    assert format_tox_ini(tox_ini) == "[tox]\nrequires =\n    tox>=4.2\n"


def test_format_env_list_simple(tox_ini: Path) -> None:
    tox_ini.write_text("[tox]\nenv_list=py39,py38\n")
    outcome = format_tox_ini(tox_ini)
    assert outcome == "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py39\n    py38\n"


def test_format_env_list_dot_version(tox_ini: Path) -> None:
    tox_ini.write_text("[tox]\nenv_list=3,3.13,3.9\n")
    outcome = format_tox_ini(tox_ini)
    assert outcome == "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    3.13\n    3.9\n    3\n"


def test_format_env_list_start_newline(tox_ini: Path) -> None:
    ok = "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py39\n    py38\n"
    tox_ini.write_text(ok)
    outcome = format_tox_ini(tox_ini)
    assert outcome == ok


def test_format_env_list_generator(tmp_path: Path) -> None:
    path = tmp_path / "tox.ini"
    path.write_text("[tox]\nenv_list={py36,py37}-django{20,21},{py36,py37}-mango{20,21},py38\n")
    outcome = format_tox_ini(path)
    msg = """\
    [tox]
    requires =
        tox>=4.2
    env_list =
        py38
        {py37, py36}-django{21, 20}
        {py37, py36}-mango{21, 20}
    """
    assert outcome == dedent(msg)


def test_tox_section_order(tox_ini: Path) -> None:
    text = """
    [tox]
    skip_missing_interpreters=true
    isolated_build=true
    requires=
     tox-magic >= 0.2
     tox-abc >= 0.1
    minversion=3.14
    skipsdist=true
    env_list=py37
    """
    tox_ini.write_text(dedent(text))
    outcome = format_tox_ini(tox_ini)
    result = """\
    [tox]
    requires =
        tox>=4.2
        tox-abc>=0.1
        tox-magic>=0.2
    env_list =
        py37
    no_package = true
    skip_missing_interpreters = true
    """
    result = dedent(result)
    assert outcome == result


@pytest.mark.parametrize(
    "key",
    [
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
    expected = f"[tox]\nrequires =\n    tox>=4.2\n{key} = {result}\n"
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

    This was previously caused by a trailing comma in the `env_list`.
    """
    tox_ini.write_text("[tox]\nenv_list=\n    py38,\n    pkg,\n[testenv:pkg]\na=b\n")
    result = format_tox_ini(tox_ini)
    assert result == "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py38\n    pkg\n\n[testenv:pkg]\na = b\n"


def test_min_version_less_requires(tox_ini: Path) -> None:
    text = """
    [tox]
    requires=
     tox >= 4.2
    min_version=3.14
    """
    tox_ini.write_text(dedent(text))
    outcome = format_tox_ini(tox_ini)
    result = """\
    [tox]
    requires =
        tox>=4.2
    """
    result = dedent(result)
    assert outcome == result


def test_min_version_greater_requires(tox_ini: Path) -> None:
    text = """
    [tox]
    requires=
     tox >= 4.2
    min_version=4.3
    """
    tox_ini.write_text(dedent(text))
    outcome = format_tox_ini(tox_ini)
    result = """\
    [tox]
    requires =
        tox>=4.3
    """
    result = dedent(result)
    assert outcome == result


def test_min_version_tox_no_spec(tox_ini: Path) -> None:
    text = """
    [tox]
    requires=
     tox
    min_version=4.3
    """
    tox_ini.write_text(dedent(text))
    outcome = format_tox_ini(tox_ini)
    result = """\
    [tox]
    requires =
        tox>=4.3
    """
    result = dedent(result)
    assert outcome == result


def test_upgrade_conflict(tox_ini: Path) -> None:
    text = """
    [tox]
    env_list=py312
    envlist=py311
    """
    tox_ini.write_text(dedent(text))
    with pytest.raises(RuntimeError, match="upgrade alias env_list also present for envlist"):
        format_tox_ini(tox_ini)
