from __future__ import annotations

import difflib
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

from tox_ini_fmt.__main__ import GREEN, RED, RESET, color_diff, run

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


def test_color_diff() -> None:
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
    diff_color = color_diff(diff)

    # Assert
    output_lines = [line.rstrip() for line in "\n".join(diff_color).splitlines()]
    assert output_lines == expected_lines


def no_color(diff: str) -> str:
    return diff


@pytest.mark.parametrize("in_place", [True, False])
@pytest.mark.parametrize("cwd", [True, False])
@pytest.mark.parametrize(
    ("start", "outcome", "output"),
    [
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,4 +1,6 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n-env_list=py311,py310\n+env_list =\n+    py311\n+    py310\n",
            id="change-core",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            "no change for {0}\n",
            id="no-change-core",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\n[testenv]\ncommands=pytest --log-format='%(asctime)s'",
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "--- {0}\n\n+++ {0}\n\n@@ -1,5 +1,7 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n+\n [testenv]\n-commands=pytest --log-format='%(asctime)s'\n"
            "+commands =\n+    pytest --log-format='%(asctime)s'\n",
            id="change-testenv",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "[tox]\nrequires =\n    tox>=4.2\n\n[testenv]\ncommands =\n    pytest --log-format='%(asctime)s'\n",
            "no change for {0}\n",
            id="no-change-testenv",
        ),
    ],
)
def test_main(  # ruff:ignore[too-many-arguments]
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    in_place: bool,
    cwd: bool,
    start: str,
    outcome: str,
    output: str,
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
) -> None:
    mocker.patch("tox_ini_fmt.__main__.color_diff", no_color)
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


NON_ASCII = "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n\n[testenv]\ncommands =\n    pytest -k 丁\n"


def test_non_ascii_round_trip(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(NON_ASCII, encoding="utf-8")

    assert run([str(tox_ini)]) == 0

    capsys.readouterr()
    assert tox_ini.read_text(encoding="utf-8") == NON_ASCII


def test_non_ascii_ignores_locale_encoding(tmp_path: Path) -> None:
    # -X warn_default_encoding turns any locale-dependent open() into an EncodingWarning, so this fails on
    # every platform rather than only where the locale encoding cannot represent the file.
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(NON_ASCII, encoding="utf-8")

    subprocess.check_call([
        sys.executable,
        "-X",
        "warn_default_encoding",
        "-W",
        "error::EncodingWarning",
        "-m",
        "tox_ini_fmt",
        str(tox_ini),
    ])


@pytest.mark.parametrize(
    ("start", "code", "output"),
    [
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list=py311,py310",
            1,
            "--- tox.ini\n\n+++ tox.ini\n\n@@ -1,4 +1,6 @@\n\n "
            "[tox]\n requires =\n     tox>=4.2\n-env_list=py311,py310\n+env_list =\n+    py311\n+    py310\n",
            id="change",
        ),
        pytest.param(
            "[tox]\nrequires =\n    tox>=4.2\nenv_list =\n    py311\n    py310\n",
            0,
            "no change for tox.ini\n",
            id="no-change",
        ),
    ],
)
def test_main_check(  # ruff:ignore[too-many-arguments]
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    mocker: MockerFixture,
    start: str,
    code: int,
    output: str,
) -> None:
    mocker.patch("tox_ini_fmt.__main__.color_diff", no_color)
    monkeypatch.chdir(tmp_path)
    tox_ini = tmp_path / "tox.ini"
    tox_ini.write_text(start)

    assert run([str(tox_ini), "--check"]) == code

    assert tox_ini.read_text() == start
    out, err = capsys.readouterr()
    assert not err
    assert out == output
