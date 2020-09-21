from textwrap import dedent

import pytest

from tox_ini_fmt.formatter import format_tox_ini
from tox_ini_fmt.formatter.section_order import explode_env_list


@pytest.mark.parametrize(
    "argument, output",
    [
        ("{py38,py37}-{,magic}\npy39-ok\npy37", ["py38", "py38-magic", "py37", "py37-magic", "py39-ok", "py37"]),
        ("py38\npy37", ["py38", "py37"]),
        ("py37\npy38", ["py37", "py38"]),
    ],
)
def test_envlist_explode(argument, output):
    result = explode_env_list(argument)
    assert result == output


def test_section_order(tox_ini):
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
        envlist = py38,py37
        e = f

        """
        )
    )
    result = format_tox_ini(tox_ini)

    expected = dedent(
        """
        [tox]
        envlist =
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
    """
    ).lstrip()
    assert result == expected
