from __future__ import annotations

from textwrap import dedent
from typing import TYPE_CHECKING

import pytest

from tox_ini_fmt.cli import ToxIniFmtNamespace
from tox_ini_fmt.formatter import format_tox_ini

if TYPE_CHECKING:
    from pathlib import Path


def test_section_order_expands_brace_env_list() -> None:
    result = format_tox_ini(
        "[tox]\nenv_list = {py38,py37}-{,magic}\n"
        "[testenv:py37-magic]\na = 1\n"
        "[testenv:py38-magic]\na = 2\n"
        "[testenv:py37]\na = 3\n"
        "[testenv:py38]\na = 4\n",
    )
    assert result == (
        "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    {py38, py37}-{, magic}\n\n"
        "[testenv:py38]\na = 4\n\n"
        "[testenv:py38-magic]\na = 2\n\n"
        "[testenv:py37]\na = 3\n\n"
        "[testenv:py37-magic]\na = 1\n"
    )


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
        encoding="utf-8",
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
    tox_ini.write_text("[tox]\nenv_list=py", encoding="utf-8")

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
        encoding="utf-8",
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
