import pytest

from tox_ini_fmt.formatter import format_tox_ini


def test_no_tox_section(tox_ini):
    tox_ini.write_text("")
    assert format_tox_ini(tox_ini) == "\n"


def test_format_envlist_simple(tox_ini):
    tox_ini.write_text("[tox]\nenvlist=py39,py38\n")
    outcome = format_tox_ini(tox_ini)
    assert outcome == "[tox]\nenvlist =\n  py39\n  py38\n"


def test_format_envlist_start_newline(tox_ini):
    ok = "[tox]\nenvlist =\n  py39\n  py38\n"
    tox_ini.write_text(ok)
    outcome = format_tox_ini(tox_ini)
    assert outcome == ok


def test_format_envlist_generator(tmp_path):
    path = tmp_path / "tox.ini"
    path.write_text("[tox]\nenvlist={py37,py36}-django{20,21},{py37,py36}-mango{20,21},py38\n")
    outcome = format_tox_ini(path)
    assert outcome == "[tox]\nenvlist =\n  {py37, py36}-django{20, 21}\n  {py37, py36}-mango{20, 21}\n  py38\n"


def test_tox_section_order(tox_ini):
    tox_ini.write_text(
        "[tox]\nskip_missing_interpreters=true\nisolated_build=true\nminversion=3.14\nskipsdist=false\nenvlist=py37"
    )
    outcome = format_tox_ini(tox_ini)
    assert (
        outcome == "[tox]\nenvlist =\n  py37\nisolated_build = true\nskipsdist = false\n"
        "skip_missing_interpreters = true\nminversion = 3.14\n"
    )


@pytest.mark.parametrize(
    "key",
    (
        "isolated_build",
        "skipsdist",
        "skip_missing_interpreters",
    ),
)
@pytest.mark.parametrize(
    "value, result",
    [
        ("True", "true"),
        ("False", "false"),
        ("TRUE", "true"),
        ("FALSE", "false"),
    ],
)
def test_tox_fmt_boolean(tox_ini, key, value, result):
    tox_ini.write_text(f"[tox]\n{key}={value}")
    outcome = format_tox_ini(tox_ini)
    expected = f"[tox]\n{key} = {result}\n"
    assert outcome == expected
