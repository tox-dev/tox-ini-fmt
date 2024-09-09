from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from tox_ini_fmt.cli import ToxIniFmtNamespace
from tox_ini_fmt.formatter import format_tox_ini
from tox_ini_fmt.formatter.section_order import explode_env_list

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("argument", "output"),
    [
        ("{py38,py37}-{,magic}\npy39-ok\npy37", ["py38", "py38-magic", "py37", "py37-magic", "py39-ok", "py37"]),
        ("py38\npy37", ["py38", "py37"]),
        ("py37\npy38", ["py37", "py38"]),
    ],
)
def test_env_list_explode(argument: str, output: list[str]) -> None:
    result = explode_env_list(argument)
    assert result == output


def test_section_order(tox_ini: Path) -> None:
    tox_ini.write_text(
        dedent(
            """
        [testenv:py37]
        c = d
        [testenv]
        a = b
        [testenv:dev]
        g = h

        [magic]
        i = j
        [tox]
        env_list = py38,py37
        e = f

        """,
        ),
    )
    result = format_tox_ini(tox_ini)

    expected = dedent(
        """
        [tox]
        requires =
            tox>=4.2
        env_list =
            py38
            py37
        e = f

        [testenv]
        a = b

        [testenv:py37]
        c = d

        [testenv:dev]
        g = h

        [magic]
        i = j
    """,
    ).lstrip()
    assert result == expected


def test_pin_missing(tox_ini: Path) -> None:
    tox_ini.write_text("[tox]\nenv_list=py")

    with pytest.raises(RuntimeError, match=r"missing tox environment\(s\) to pin missing_1, missing_2"):
        format_tox_ini(tox_ini, ToxIniFmtNamespace(pin_toxenvs=["missing_1", "missing_2"]))


def test_pin(tox_ini: Path) -> None:
    tox_ini.write_text(
        "[tox]\nenv_list=py38,pkg,py,py39,pypy3,pypy,pin,extra\n"
        "[testenv:py38]\ne=f\n"
        "[testenv:pkg]\nc=d\n"
        "[testenv:py]\ng=h\n"
        "[testenv:py39]\ni=j\n"
        "[testenv:pypy3]\nk=l\n"
        "[testenv:pypy]\nm=n\n"
        "[testenv:pin]\na=b\n"
        "[testenv:extra]\no=p\n",
    )
    result = format_tox_ini(tox_ini, ToxIniFmtNamespace(pin_toxenvs=["pin", "pkg"]))

    expected = dedent(
        """
        [tox]
        requires =
            tox>=4.2
        env_list =
            pin
            pkg
            py39
            py38
            py
            pypy3
            pypy
            extra

        [testenv:pin]
        a = b

        [testenv:pkg]
        c = d

        [testenv:py39]
        i = j

        [testenv:py38]
        e = f

        [testenv:py]
        g = h

        [testenv:pypy3]
        k = l

        [testenv:pypy]
        m = n

        [testenv:extra]
        o = p
    """,
    ).lstrip()
    assert result == expected
