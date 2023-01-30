from __future__ import annotations

import os

import pytest

from tox_ini_fmt.__main__ import run


def test_platform_default(tox_ini):
    """If the ini file has no newlines, the platform default may be inserted."""

    tox_ini.write_bytes(b"[tox]")
    run([str(tox_ini)])
    assert tox_ini.read_bytes() == f"[tox]{os.linesep}".encode()


@pytest.mark.parametrize("newline", ["\r\n", "\n", "\r"])
def test_line_endings(tox_ini, newline):
    """The ini file's existing newlines must be respected when reformatting."""

    original_text = f"[tox]{newline}envlist=py39"
    expected_text = f"[tox]{newline}envlist ={newline}    py39{newline}"
    tox_ini.write_bytes(original_text.encode("utf8"))
    run([str(tox_ini)])
    assert tox_ini.read_bytes() == expected_text.encode("utf8")


def test_mixed_line_endings(tox_ini):
    """If mixed line endings are found, the first one in the tuple should be used.

    Note that this does not mean the first newline in the file will be used!
    Python does not report the newlines in the order they're encountered.
    """

    original_text = "[tox]\r\n \r \nenvlist=py39"
    expected_text = "[tox]!!envlist =!!    py39!!"
    tox_ini.write_bytes(original_text.encode("utf8"))
    with tox_ini.open("rt") as file:
        file.read()
        assert set(file.newlines) == {"\r", "\n", "\r\n"}
        first_newline = file.newlines[0]

    expected_text = expected_text.replace("!!", first_newline)
    run([str(tox_ini)])
    assert tox_ini.read_bytes() == expected_text.encode("utf8")