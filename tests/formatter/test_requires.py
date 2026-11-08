from __future__ import annotations

import pytest

from tox_ini_fmt.formatter.requires import requires


@pytest.mark.parametrize(
    ("value", "result"),
    [
        pytest.param("", [], id="empty"),
        pytest.param("\t", [], id="tab"),
        pytest.param("\n\t\n", [], id="blank-lines"),
        pytest.param("b\na\n", ["a", "b"], id="sorted"),
        pytest.param("a\nb\n", ["a", "b"], id="already-sorted"),
        pytest.param("A\na\n", ["A", "a"], id="case-kept"),
        pytest.param("\nA\n\n\nb\n\n", ["A", "b"], id="skips-blank-lines"),
        pytest.param(
            (
                'packaging>=20.0;python_version>"3.4"\n'
                "xonsh>=0.9.16;python_version > '3.4' and python_version != '3.9'\n"
                "pytest-xdist>=1.31.0\n"
            ),
            [
                "pytest-xdist>=1.31",
                'packaging>=20; python_version > "3.4"',
                'xonsh>=0.9.16; python_version > "3.4" and python_version != "3.9"',
            ],
            id="environment-markers",
        ),
        pytest.param("pytest>=6.0.0", ["pytest>=6"], id="ge-trims-patch"),
        pytest.param("pytest==6.0.0", ["pytest==6"], id="eq-trims-patch"),
        pytest.param("pytest~=6.0.0", ["pytest~=6.0.0"], id="compatible-kept"),
    ],
)
def test_requires_fmt(value: str, result: list[str]) -> None:
    outcome = requires([i.strip() for i in value.splitlines() if i.strip()])
    assert outcome == result
