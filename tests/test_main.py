from __future__ import annotations

import difflib

import pytest

import tox_ini_fmt.__main__
from tox_ini_fmt.__main__ import GREEN, RED, RESET, color_diff, detect_line_ending, run


def test_color_diff():
    # Arrange
    before = """
    abc
    def
    ghi
"""
    after = """
    abc
    abc
    def
"""
    diff = difflib.unified_diff(before.splitlines(), after.splitlines())
    expected_lines = f"""
{RED}---
{RESET}
{GREEN}+++
{RESET}
@@ -1,4 +1,4 @@


     abc
{GREEN}+    abc{RESET}
     def
{RED}-    ghi{RESET}
""".strip().splitlines()

    # Act
    diff = color_diff(diff)

    # Assert
    output_lines = [line.rstrip() for line in "\n".join(diff).splitlines()]
    assert output_lines == expected_lines


def no_color(diff):
    return diff


@pytest.mark.parametrize("in_place", [True, False])
@pytest.mark.parametrize("cwd", [True, False])
@pytest.mark.parametrize(
    ("start", "outcome", "output"),
    [
        (
            "[tox]\nenvlist=py39,py38",
            "[tox]\nenvlist =\n    py39\n    py38\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,2 +1,4 @@\n\n "
            "[tox]\n-envlist=py39,py38\n+envlist =\n+    py39\n+    py38\n",
        ),
        ("[tox]\nenvlist =\n    py39\n    py38\n", "[tox]\nenvlist =\n    py39\n    py38\n", "no change for {0}\n"),
        (
            "[testenv]\ncommands=pytest --log-format='%(asctime)s'",
            "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,2 +1,3 @@\n\n "
            "[testenv]\n-commands=pytest --log-format='%(asctime)s'\n"
            "+commands =\n+    pytest --log-format='%(asctime)s'\n",
        ),
        (
            "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "no change for {0}\n",
        ),
    ],
)
def test_main(tmp_path, capsys, in_place, start, outcome, output, monkeypatch, cwd):
    monkeypatch.setattr(tox_ini_fmt.__main__, "color_diff", no_color)
    if cwd:
        monkeypatch.chdir(tmp_path)
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)
    args = [str(tox_ini)]
    if not in_place:
        args.append("--stdout")

    result = run(args)
    assert result == (0 if start == outcome else 1)

    out, err = capsys.readouterr()
    assert not err

    if in_place:
        name = "tox.ini" if cwd else str(tmp_path / "tox.ini")
        output = output.format(name)
        assert tox_ini.read_text() == outcome
        assert out == output
    else:
        assert out == outcome


def test_detect_line_ending_more_lf(tmp_path):
    more_lf_text = "asdf\r\nqwertz\n12345\r\n67890\nyxcvb\nhjkl".encode(encoding="ansi")
    tox_ini = tmp_path / "tox.ini"
    with open(str(tox_ini), "wb") as f:
        f.write(more_lf_text)
    assert "\n" == detect_line_ending(str(tox_ini))


more_lf_tox_ini = "[testenv]\ncommands =\r\n    pytest --log-format='%(asctime)s'\n".encode(encoding="ansi")
only_lf_tox_ini = "[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n".encode(encoding="ansi")
more_crlf_tox_ini = "[testenv]\r\ncommands =\n    pytest --log-format='%(asctime)s'\r\n".encode(encoding="ansi")
only_crlf_tox_ini = "[testenv]\r\ncommands =\r\n    pytest --log-format='%(asctime)s'\r\n".encode(encoding="ansi")


def test_main_auto_line_ending_more_crlf(tmp_path):
    tox_ini = tmp_path / "tox.ini"
    with open(str(tox_ini), "wb") as f:
        f.write(more_crlf_tox_ini)
    args = [str(tox_ini)]
    run(args)
    with open(str(tox_ini), "rb") as f:
        content = f.read()

    assert content != more_crlf_tox_ini
    assert content == only_crlf_tox_ini


def test_main_auto_line_ending_more_lf(tmp_path):
    tox_ini = tmp_path / "tox.ini"
    with open(str(tox_ini), "wb") as f:
        f.write(more_lf_tox_ini)
    args = [str(tox_ini)]
    run(args)
    with open(str(tox_ini), "rb") as f:
        content = f.read()

    assert content != more_lf_tox_ini
    assert content == only_lf_tox_ini


def test_main_force_lf_line_ending(tmp_path):
    tox_ini = tmp_path / "tox.ini"
    with open(str(tox_ini), "wb") as f:
        f.write(only_crlf_tox_ini)
    args = [str(tox_ini), "-l", "lf"]
    run(args)
    with open(str(tox_ini), "rb") as f:
        content = f.read()

    assert content != only_crlf_tox_ini
    assert content == only_lf_tox_ini


def test_main_lf_to_lf_line_ending_no_change(tmp_path):
    tox_ini = tmp_path / "tox.ini"
    with open(str(tox_ini), "wb") as f:
        f.write(only_lf_tox_ini)
    args = [str(tox_ini), "-l", "lf"]
    run(args)
    with open(str(tox_ini), "rb") as f:
        content = f.read()

    assert content == only_lf_tox_ini


def test_main_crlf_to_crlf_line_ending_no_change(tmp_path):
    tox_ini = tmp_path / "tox.ini"
    with open(str(tox_ini), "wb") as f:
        f.write(only_crlf_tox_ini)
    args = [str(tox_ini), "-l", "crlf"]
    run(args)
    with open(str(tox_ini), "rb") as f:
        content = f.read()

    assert content == only_crlf_tox_ini
