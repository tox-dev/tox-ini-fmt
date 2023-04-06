from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import pytest

from tox_ini_fmt.formatter import format_tox_ini
from tox_ini_fmt.formatter.test_env import to_ordered_list
from tox_ini_fmt.formatter.util import to_py_dependencies


def test_no_tox_section(tox_ini: Path) -> None:
    tox_ini.write_text("")
    assert format_tox_ini(tox_ini) == "\n"


def test_format_test_env(tox_ini: Path) -> None:
    content = dedent(
        """
    usedevelop = True
    skip_install =\tFalse
    parallel_show_output = false
    commands = \te
      \tf  \\
      \t \\
      \t g
    extras = \tc,d
    description = \tdesc\t
    deps = \tb\t
      \ta\t
    basepython=\tpython3.8\t
    passenv=z y x
    setenv= C=D
            E =F

            A = B
    """,
    ).strip()
    tox_ini.write_text(f"[testenv]\n{content}")
    outcome = format_tox_ini(tox_ini)
    expected = dedent(
        """
        [testenv]
        description = desc
        basepython = python3.8
        skip_install = false
        usedevelop = true
        deps =
            a
            b
        extras =
            c
            d
        parallel_show_output = false
        passenv =
            x
            y
            z
        setenv =
            A = B
            C = D
            E = F
        commands =
            e
            f \\
              g
        """,
    ).lstrip()
    assert outcome == expected


@pytest.mark.parametrize(
    ("arg", "output"),
    [
        ("", ""),
        ("\t", ""),
        ("\n", ""),
        ("a", "\na"),
        (" a ", "\na"),
        ("b,a", "\na\nb"),
        ("a,b", "\na\nb"),
        ("b\n  a,c", "\na\nb\nc"),
        ("c\n  c,c", "\nc"),
        ("\n b\n a\n a: b\n b: c\n a,b: g\n b, a: h\n ", "\na\nb\na: b\nb: c\na, b: g\na, b: h"),
    ],
)
def test_extras(arg: str, output: str) -> None:
    result = to_ordered_list(arg)
    assert result == output


@pytest.mark.parametrize(
    ("key", "before", "pre", "post", "expected"),
    [
        (
            "setenv",
            "\n    A = B",
            "C=D",
            "E=F",
            "\n    {[testenv:x]X}\n    {[testenv]setenv}\n    C = D\n    E = F",
        ),
        (
            "passenv",
            "\n    A",
            "C",
            "E",
            "\n    {[testenv:x]X}\n    {[testenv]passenv}\n    C\n    E",
        ),
        (
            "deps",
            "\n    A",
            "C",
            "B",
            "\n    {[testenv:x]X}\n    {[testenv]deps}\n    B\n    C",
        ),
        (
            "extras",
            "\n    A",
            "B",
            "C",
            "\n    {[testenv:x]X}\n    {[testenv]extras}\n    B\n    C",
        ),
    ],
)
def test_format_test_env_ref(tox_ini: Path, key: str, before: str, pre: str, post: str, expected: str) -> None:
    text = (
        f"[testenv]\n{key}={before}\n[testenv:py]"
        f"\n{key}=\n {pre}\n {{[testenv:x]X}}\n {{[testenv]{key}}}\n {post}\n"
    )
    tox_ini.write_text(text)
    outcome = format_tox_ini(tox_ini)
    expected = f"[testenv]\n{key} ={before}\n\n[testenv:py]\n{key} ={expected}\n"
    assert outcome == expected


def test_fail_on_bad_set_env(tox_ini: Path) -> None:
    tox_ini.write_text("[testenv]\nsetenv = A")
    with pytest.raises(RuntimeError, match="invalid line A in setenv"):
        format_tox_ini(tox_ini)


def test_deps_conditional() -> None:
    result = to_py_dependencies(
        "\ncoverage,codecov: coverage\ncodecov: codecov"
        "\n-r{toxinidir}/test-requirements.txt\n-r{toxinidir}/dev-requirements.txt"
        "\nvirtue\nb",
    )
    assert (
        result == "\n-r{toxinidir}/dev-requirements.txt\n-r{toxinidir}/test-requirements.txt"
        "\nb\nvirtue"
        "\ncodecov: codecov\ncodecov, coverage: coverage"
    )


def test_python_req_sort_by_name() -> None:
    result = to_py_dependencies("pytest-cov\npytest\npytest-magic>=1\npytest>=1")
    assert result == "\npytest\npytest>=1\npytest-cov\npytest-magic>=1"


def test_depends_ordering(tox_ini: Path) -> None:
    tox_ini.write_text("[testenv]\ndepends =\n py311\n py312\n py39\n p310")
    outcome = format_tox_ini(tox_ini)
    assert outcome == "[testenv]\ndepends =\n    py312\n    py311\n    py39\n    p310\n"
