from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from tox_ini_fmt.__main__ import run

if TYPE_CHECKING:
    from pathlib import Path


def test_platform_default(tox_ini: Path) -> None:
    """If the ini file has no newlines, the platform default may be inserted."""

    tox_ini.write_bytes(b"[tox]")
    run([str(tox_ini)])
    assert tox_ini.read_bytes() == f"[tox]{os.linesep}requires ={os.linesep}    tox>=4.2{os.linesep}".encode()


@pytest.mark.parametrize("newline", ["\r\n", "\n", "\r"])
def test_line_endings(tox_ini: Path, newline: str) -> None:
    """The ini file's existing newlines must be respected when reformatting."""

    original_text = f"[tox]{newline}requires ={newline}    tox>=4.2{newline}env_list=py39"
    expected_text = f"[tox]{newline}requires ={newline}    tox>=4.2{newline}env_list ={newline}    py39{newline}"
    tox_ini.write_bytes(original_text.encode("utf8"))
    run([str(tox_ini)])
    assert tox_ini.read_bytes() == expected_text.encode("utf8")


def test_mixed_line_endings(tox_ini: Path) -> None:
    """If mixed line endings are found, the first one in the tuple should be used.

    Note that this does not mean the first newline in the file will be used!
    Python does not report the newlines in the order they're encountered.
    """

    original_text = "[tox]\r\n \r \nenv_list=py39"
    expected_text = "[tox]!!requires =!!    tox>=4.2!!env_list =!!    py39!!"
    tox_ini.write_bytes(original_text.encode("utf8"))
    with tox_ini.open("rt") as file:
        file.read()
        assert not isinstance(file.newlines, str)
        assert file.newlines is not None
        assert set(file.newlines) == {"\r", "\n", "\r\n"}
        first_newline = file.newlines[0]

    expected_text = expected_text.replace("!!", first_newline)
    run([str(tox_ini)])
    assert tox_ini.read_bytes() == expected_text.encode("utf8")
